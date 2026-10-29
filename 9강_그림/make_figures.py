from pathlib import Path
import math
from html import escape
out=Path(__file__).parent
def t(x,y,s,n=18): return f'<text x="{x}" y="{y}" font-size="{n}" text-anchor="middle" fill="#263445">{escape(s)}</text>'
def l(x,y,u,v): return f'<line x1="{x}" y1="{y}" x2="{u}" y2="{v}" stroke="#9aabb9" stroke-width="2"/>'
def save(name,w,h,p): (out/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="font-family:Malgun Gothic,sans-serif"><rect width="100%" height="100%" fill="white"/>'+''.join(p)+'</svg>',encoding='utf-8')
p=[t(600,30,'활성화 함수: 가중합 z → 출력 a',24)]
fs=[('계단함수',lambda x:int(x>=0),(-.25,1.25)),('부호함수',lambda x:1 if x>=0 else -1,(-1.5,1.5)),('선형함수',lambda x:x,(-5,5)),('시그모이드',lambda x:1/(1+math.exp(-x)),(-.25,1.25)),('tanh',math.tanh,(-1.5,1.5)),('ReLU',lambda x:max(0,x),(-1,5))]
for i,(title,f,(lo,hi)) in enumerate(fs):
    ox=65+i%3*400;oy=85+i//3*280
    X=lambda x:ox+(x+5)*30
    Y=lambda y:oy+185-(y-lo)/(hi-lo)*185
    p += [t(ox+150,oy-15,title,21),l(ox,Y(0),ox+300,Y(0)),l(X(0),oy,X(0),oy+185),t(ox+150,oy+230,'가중합 z',16),t(ox-25,oy+10,'a',16)]
    for v in [-5,0,5]:p.append(t(X(v),oy+207,str(v),13))
    for v in [lo,0,hi]:p.append(t(ox-25,Y(v)+4,f'{v:g}',12))
    groups=[[-5+j/40 for j in range(200)],[j/40 for j in range(201)]] if i<2 else [[-5+j/40 for j in range(401)]]
    for g in groups:
        coords=' '.join(f'{X(x):.2f},{Y(f(x)):.2f}' for x in g)
        p.append(f'<polyline points="{coords}" fill="none" stroke="#2166ac" stroke-width="3"/>')
save('01_활성화함수.svg',1200,640,p)
p=[t(600,30,'AND·OR는 직선 하나로 분리 / XOR는 직선 하나로 분리 불가',23),t(600,60,'파란 원 = 정답 0    주황 삼각형 = 정답 1',17)]
for i,(name,labs) in enumerate([('AND',[0,0,0,1]),('OR',[0,1,1,1]),('XOR',[0,1,1,0])]):
    ox=65+400*i;oy=125
    X=lambda v:ox+v*230
    Y=lambda v:oy+230-v*230
    p += [t(ox+115,100,name,23),l(ox-20,Y(0),ox+265,Y(0)),l(ox,oy-15,ox,oy+250),t(ox+115,410,'입력 x₁',17),t(ox-20,oy-16,'입력 x₂',17)]
    if i==0:p.append(l(X(.5),Y(1),X(1),Y(.5)))
    elif i==1:p.append(l(X(0),Y(.5),X(.5),Y(0)))
    else:
        p.append(f'<polygon points="{X(0)},{Y(.5)} {X(0)},{Y(1)} {X(.5)},{Y(1)} {X(1)},{Y(.5)} {X(1)},{Y(0)} {X(.5)},{Y(0)}" fill="#fff0e1"/>')
        p += [l(X(0),Y(.5),X(.5),Y(0)),l(X(.5),Y(1),X(1),Y(.5)),t(ox+115,450,'음영: 두 경계 사이가 출력 1',16)]
    for v in [0,1]:p += [t(X(v),Y(0)+28,str(v),14),t(ox-25,Y(v)+5,str(v),14)]
    for (a,b),lab in zip([(0,0),(0,1),(1,0),(1,1)],labs):
        x,y=X(a),Y(b)
        p.append(f'<polygon points="{x},{y-11} {x-11},{y+10} {x+11},{y+10}" fill="#d66016"/>' if lab else f'<circle cx="{x}" cy="{y}" r="10" fill="#2166ac"/>')
        p.append(t(x+20,y-12,str(lab),17))
save('02_AND_OR_XOR.svg',1200,480,p)
p=[t(500,35,'전방향 신경망: 입력 → 은닉층 → 출력',25)]
layers=[[(130,150),(130,290)],[(500,100),(500,220),(500,340)],[(870,220)]]
for a,b in zip(layers,layers[1:]):
    for x,y in a:
        for u,v in b:p.append(l(x,y,u,v))
for i,layer in enumerate(layers):
    for j,(x,y) in enumerate(layer):
        color=['#d8e8f6','#ffe2c7','#d9ebdb'][i]
        p.append(f'<circle cx="{x}" cy="{y}" r="30" fill="{color}" stroke="#455a64"/>')
        p.append(t(x,y+6,'x'+str(j+1) if i==0 else ('h'+str(j+1) if i==1 else 'ŷ')))
for x,title,sub in [(130,'입력층','관측한 특징값'),(500,'은닉층','가중합 → 비선형 변환'),(870,'출력층','최종 예측')]:p += [t(x,410,title,22),t(x,443,sub,17)]
save('03_다층신경망.svg',1000,470,p)
print('Created 3 SVG figures.')
