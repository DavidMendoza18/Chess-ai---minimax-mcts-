"""Build portfolio summaries from archived logs; never rerun timed searches."""
from pathlib import Path
import csv, re, sys, statistics, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import chess, chess.svg
from posiciones import POSITIONS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cairosvg

def field(t, label):
    match = re.search(r'^'+re.escape(label)+r': (.+)$', t, re.M)
    if not match: raise ValueError(f'Missing {label}')
    return match[1].strip()

def write(p, text):
    (ROOT/p).parent.mkdir(parents=True, exist_ok=True)
    (ROOT/p).write_text(text, encoding='utf-8')

verification=(ROOT/'resultados_20/verificacion_mcts.txt').read_text()
checks={int(n): (m, v) for n,m,v in re.findall(r'Position: (\d+) - .*?MCTS move: (\S+).*?Forces mate within 3 moves: (YES|NO)',verification,re.S)}
rows=[]
for n,(name,fen) in POSITIONS.items():
    r={'position':n,'name':name,'fen':fen,'pieces':len(chess.Board(fen).piece_map())}
    for key,filename in [('minimax',f'minimax_posicion_{n}.txt'),('alpha_beta',f'minimax_ab_posicion_{n}_depth5.txt'),('mcts',f'mcts_posicion_{n}.txt')]:
        t=(ROOT/'resultados_20'/filename).read_text()
        assert field(t,'FEN')==fen
        b=chess.Board(fen);assert b.is_valid()
        move=field(t,'Selected move');b.parse_san(move)
        r[key+'_move']=move;r[key+'_seconds']=float(field(t,'Time').split()[0])
        if key=='minimax': assert field(t,'Depth (plies)')=='3'
        if key=='mcts':
            assert field(t,'Simulations')=='1000' and field(t,'Rollout limit (plies)')=='80' and field(t,'Seed')=='42'
        if key=='alpha_beta':
            assert field(t,'Depth (plies)')=='5' and field(t,'Time limit')=='60.0 seconds'
            r['alpha_beta_reported_mate']=field(t,'Forced mate within search depth')
            r['example_line']=field(t,'Example line')
            assert r['example_line'].split()[0]==move
            for san in r['example_line'].split():b.push_san(san)
            assert b.is_checkmate()
    assert checks[n][0]==r['mcts_move']
    r['mcts_verified_mate']=checks[n][1]
    r['minimax_matches_alpha_beta']=r['minimax_move']==r['alpha_beta_move']
    rows.append(r)
with (ROOT/'data/summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
keys=['minimax','alpha_beta','mcts'];labels=['Minimax · 3 plies','Alpha-beta · 5 plies','MCTS · 1,000 simulations'];colors=['#237a91','#d07838','#6756a4']
stats={k:{'runs':20,'median_seconds':statistics.median(r[k+'_seconds'] for r in rows),'min_seconds':min(r[k+'_seconds'] for r in rows),'max_seconds':max(r[k+'_seconds'] for r in rows)} for k in keys}
write('data/statistics.json',json.dumps(stats,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(10,4.6),layout='constrained')
for k,l,c in zip(keys,labels,colors):ax.plot(range(1,21),[r[k+'_seconds'] for r in rows],marker='o',label=l,color=c,linewidth=1.4,markersize=4)
ax.set(yscale='log',xlabel='Position number',ylabel='Recorded search time (seconds, log scale)',title='20 positions · archived search times',xticks=range(1,21));ax.grid(axis='y',alpha=.2);ax.legend(loc='upper right',fontsize=9)
fig.savefig(ROOT/'figures/runtime.png',dpi=180);fig.savefig(ROOT/'figures/runtime.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3.5),layout='constrained')
v=[stats[k]['median_seconds'] for k in keys];bars=ax.barh(labels,v,color=colors)
ax.bar_label(bars,labels=[f'{x:.4f} s' for x in v],padding=5);ax.set(xlim=(0,max(v)*1.22),xlabel='Median recorded seconds',title='Different workloads, not an equal-budget speed test');ax.invert_yaxis()
fig.savefig(ROOT/'figures/median_times.png',dpi=180);plt.close(fig)
# Three views of the same board, with arrows for the three recorded selections.
from PIL import Image
panels=[]
for key,color in zip(keys,colors):
    b=chess.Board(POSITIONS[2][1]);m=b.parse_san(rows[1][key+'_move'])
    svg=chess.svg.board(b,arrows=[chess.svg.Arrow(m.from_square,m.to_square,color=color)],size=420)
    write(f'figures/evergreen_{key}.svg',svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(ROOT/f'figures/evergreen_{key}.png'))
    panels.append(Image.open(ROOT/f'figures/evergreen_{key}.png').convert('RGB'))
canvas=Image.new('RGB',(1260,420),'white')
for i,p in enumerate(panels):canvas.paste(p,(420*i,0))
canvas.save(ROOT/'figures/evergreen_comparison.png')
# File hashes identify the exact original sources and logs used.
files=sorted(list(ROOT.glob('*.py'))+list((ROOT/'resultados_20').glob('*.txt'))+list((ROOT/'archive/early_runs').glob('*.txt')))
write('data/source_hashes.json',json.dumps({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},indent=2)+'\n')
write('data/validation.json',json.dumps({'checks':'Portfolio preparation checks, not original timed runs','archived_search_logs':60,'fens_match_position_definitions':60,'selected_moves_legal':60,'alpha_beta_example_lines_end_in_checkmate':20,'mcts_verification_records_matched':20,'note':'Line replay verifies legal checkmate examples, not all defensive branches or uniqueness.'},indent=2)+'\n')
header='| # | Position | Minimax d3 | Seconds | Alpha-beta d5 | Seconds | MCTS | Seconds | MCTS mate ≤5 plies |\n|---|---|---|---:|---|---:|---|---:|---|\n'
table=header+''.join(f"| {r['position']} | {r['name']} | {r['minimax_move']} | {r['minimax_seconds']:.4f} | {r['alpha_beta_move']} | {r['alpha_beta_seconds']:.4f} | {r['mcts_move']} | {r['mcts_seconds']:.4f} | {r['mcts_verified_mate']} |\n" for r in rows)
write('docs/results.md','# Results across 20 positions\n\nSource: the original logs in [`resultados_20`](../resultados_20/). One recorded run per algorithm per position. Alpha-beta reported a forced mate in all 20 runs. The final column comes from the archived MCTS verification log.\n\n'+table+'\nA NO means no forced mate within the five-ply horizon under the verifier, not necessarily a losing move. No unique-key or shortest-mate claim is made.\n\n[Download the full CSV](../data/summary.csv)\n')
print(json.dumps(stats));print('Minimax same selected move as alpha-beta:',sum(r['minimax_matches_alpha_beta'] for r in rows))
# PDF: four deliberate pages.
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image as RImage,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors as C
from reportlab.lib.enums import TA_LEFT
styles=getSampleStyleSheet();styles['Title'].textColor=C.HexColor('#15394b');styles['Heading1'].textColor=C.HexColor('#15394b');styles['BodyText'].leading=14
story=[]
def p(t,style='BodyText'):story.append(Paragraph(t,styles[style]));story.append(Spacer(1,8))
def im(path,w,h):story.append(RImage(str(ROOT/path),width=w,height=h));story.append(Spacer(1,8))
def tab(data,widths):
    t=Table(data,colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C.HexColor('#15394b')),('TEXTCOLOR',(0,0),(-1,0),C.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[C.HexColor('#edf3f5'),C.white]),('VALIGN',(0,0),(-1,-1),'TOP')]));story.append(t);story.append(Spacer(1,10))
p('Chess search on 20 tactical positions','Title');p('David Mendoza | University of Illinois Chicago | Fall 2026','Heading2')
p('Portfolio analysis of archived Python experiments','Heading2')
p('I compared plain Minimax at depth three, Minimax with alpha-beta pruning at depth five, and Monte Carlo Tree Search with 1,000 simulations. This report summarizes my saved outputs, rather than replacing them with new timing measurements.')
tab([['Method','Completed logs','Median time'],*[[l.replace(' · ',' / '),'20 / 20',f"{stats[k]['median_seconds']:.4f} s"] for k,l in zip(keys,labels)]],[300,90,110])
im('figures/runtime.png',500,230)
p('All 20 alpha-beta logs report a forced mate within five plies. The archived verification script confirms the same bounded-mate property for 2 of the 20 MCTS selections (positions 15 and 20). Plain Minimax selections were not all separately checked for this property in the archived verifier.')
p('The search budgets differ. These measurements do not isolate the speedup from pruning and do not establish general playing strength. Each position has only one recorded run per configuration.')
story.append(PageBreak())
p('Recorded decisions and times','Title')
p('MM: Minimax, depth 3. AB: alpha-beta, depth 5. MC: MCTS, seed 42. Times are seconds. MC mate is the archived verification outcome within five total plies.')
tab([['#','MM move','MM sec','AB move','AB sec','MC move','MC sec','MC mate']]+[[str(r['position']),r['minimax_move'],f"{r['minimax_seconds']:.4f}",r['alpha_beta_move'],f"{r['alpha_beta_seconds']:.4f}",r['mcts_move'],f"{r['mcts_seconds']:.4f}",r['mcts_verified_mate']] for r in rows],[25,70,55,70,55,70,55,50])
p('The companion CSV includes each position name, FEN, piece count, example line and recorded outcome. Source: resultados_20/. A matching first move is not itself proof of a unique or shortest forced mate.')
story.append(PageBreak())
p('Case study: The Evergreen Game','Title')
p('Position 2 | White to move | 21 pieces','Heading2')
im('figures/evergreen_comparison.png',510,170)
p('Left: Minimax Be2+. Center: alpha-beta Bf5+. Right: MCTS Ba6+. Each panel starts from the same position; arrows show the recorded first move.')
e=rows[1]
tab([['Method','Move','Archived time'],['Minimax, depth 3',e['minimax_move'],f"{e['minimax_seconds']:.4f} s"],['Alpha-beta, depth 5',e['alpha_beta_move'],f"{e['alpha_beta_seconds']:.4f} s"],['MCTS, 1,000 simulations',e['mcts_move'],f"{e['mcts_seconds']:.4f} s"]],[270,100,130])
p('One recorded mating continuation','Heading2');p('1. Bf5+ Ke8 2. Bd7+ Kf8 3. Bxe7#')
p('This line has five plies: White moves three times and Black replies twice. The alpha-beta search reported a winning terminal score of 10000. The example line was replayed during portfolio preparation and legally ends in checkmate; a single line alone does not prove that every defense loses.')
p('The archived verifier reports NO for Ba6+ within the same five-ply horizon. MCTS returns the most visited root move after random rollouts; those samples are not an exhaustive proof against all legal defenses. Depth-three Minimax cannot reach the final position of this five-ply example.')
p('What this comparison shows','Heading2');p('Giving check and preserving a short forced mate are different objectives. The observed choices illustrate the effects of search horizon and sampling. The logs do not contain visit counts or rollout traces, so they do not establish a specific causal explanation for why Ba6+ was preferred.')
story.append(PageBreak())
p('Methods, earlier runs, and scope','Title')
p('Implementation','Heading2');p('Both Minimax variants use material scores: pawn 1, knight 3, bishop 3, rook 5, queen 9. Terminal wins have scores +10000 for White or -10000 for Black. Alpha-beta orders checks, captures and promotions before other moves and stops inconclusively if its deadline is reached. It does not rank mates by distance.')
p('MCTS uses UCT selection, random expansion and random legal rollouts. After at most 80 rollout plies, a nonterminal board receives 0.5 + 0.5 tanh(material / 10). Rewards are backed up from the previous mover\'s perspective. The final root choice is the most visited child. Each archived call uses seed 42.')
p('Earlier board-size exploration','Heading2')
tab([['Pieces','Minimax d4','MCTS / 1,000 sims'],['4','0.1280 s / Kf2','3.1625 s / Kf2'],['10','0.2049 s / Ke2','4.3022 s / Ke2'],['32','4.1861 s / Nh3','5.6592 s / a4']],[80,210,210])
p('These six earlier logs are retained separately. Their MCTS seed and exact original code version are not recorded. They describe three different boards, not a controlled experiment isolating piece count. Their evaluations are preserved without treating them as independently verified scores.')
p('Reproduction and provenance','Heading2');p('From the repository root, install requirements.txt and run the commands in README.md. The report-generation script rebuilds CSVs, figures and this PDF from existing logs. It checks all 60 FENs and selected moves, and replays all 20 alpha-beta example lines. These are new portfolio-preparation checks, not new historical experiments.')
p('Course-provided positions; Python and python-chess; experiments run by David Mendoza in WSL Ubuntu. AI assistance was used for code development, troubleshooting and documentation. This portfolio is a personal record and does not claim inclusion in the final group poster. Original machine specifications and package versions were not captured in the logs. No classmate measurements or reports are included.')
p('Limits','Heading2');p('There is one MCTS seed, unequal search budgets, a material-only cutoff evaluation, and no independent-engine validation. The MCTS verifier reuses alpha-beta. No claim is made that each solution is unique, shortest, or historically identical to a printed diagram.')
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(C.HexColor('#526575'));c.drawString(48,25,'DAVID MENDOZA / CHESS SEARCH');c.drawRightString(564,25,str(d.page))
SimpleDocTemplate(str(ROOT/'reports/Chess_Search_Report.pdf'),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=40,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
