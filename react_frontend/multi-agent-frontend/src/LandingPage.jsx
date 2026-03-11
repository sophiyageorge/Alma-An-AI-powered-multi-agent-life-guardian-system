import { useState, useEffect, useRef } from "react";
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";
import AuthModel from "./components/auth/AuthModel";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  :root {
    --teal: #4fc3f7; --teal2: #00d4d8; --pink: #f06292; --pink2: #ff4d7a;
    --purple: #9c6ef0; --green: #4caf82; --bg1: #080c28; --text: #e8eeff;
    --dim: rgba(232,238,255,0.5);
  }
  body { background: #080c28; margin:0; }
  .gr {
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg,#080c28 0%,#0d1245 35%,#130d38 65%,#080c28 100%);
    color: var(--text); min-height:100vh; overflow-x:hidden; position:relative;
  }
  .gr::before {
    content:''; position:fixed; inset:0;
    background-image: radial-gradient(circle,rgba(255,255,255,.035) 1px,transparent 1px);
    background-size:44px 44px; pointer-events:none; z-index:0;
  }
  .blob { position:fixed; border-radius:50%; filter:blur(110px); pointer-events:none; z-index:0; }
  .b1 { width:650px;height:650px; background:radial-gradient(circle,rgba(79,195,247,.1),transparent 70%); top:-180px;left:-120px; animation:bf 11s ease-in-out infinite; }
  .b2 { width:520px;height:520px; background:radial-gradient(circle,rgba(156,110,240,.09),transparent 70%); top:250px;right:-160px; animation:bf 11s -5.5s ease-in-out infinite; }
  .b3 { width:420px;height:420px; background:radial-gradient(circle,rgba(240,98,146,.07),transparent 70%); bottom:80px;left:35%; animation:bf 11s -2.5s ease-in-out infinite; }
  @keyframes bf { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-35px) scale(1.04)} }

  /* NAV */
  .nav {
    position:fixed; top:0; width:100%; z-index:200;
    padding:1rem 4rem; display:flex; align-items:center; justify-content:space-between;
    background:rgba(8,12,40,.75); backdrop-filter:blur(22px);
    border-bottom:1px solid rgba(79,195,247,.09);
  }
  .nlogo { display:flex; align-items:center; gap:.6rem; font-size:1.25rem; font-weight:700; color:#fff; }
  .nico {
    width:34px;height:34px;border-radius:10px;
    background:linear-gradient(135deg,var(--teal2),var(--teal));
    display:flex;align-items:center;justify-content:center;font-size:.95rem;
    box-shadow:0 0 18px rgba(0,212,216,.28);
  }
  .nlogo span{color:var(--teal2);}
  .nlinks{display:flex;gap:2.2rem;}
  .nl{font-size:.83rem;font-weight:500;color:var(--dim);cursor:pointer;transition:color .2s;}
  .nl:hover{color:#fff;}
  .nbtn{
    padding:.52rem 1.4rem;border-radius:8px;
    background:linear-gradient(135deg,var(--teal2),var(--teal));
    border:none;color:#fff;font-family:'Poppins',sans-serif;
    font-size:.78rem;font-weight:600;cursor:pointer;
    box-shadow:0 4px 18px rgba(0,212,216,.28);transition:all .3s;
  }
  .nbtn:hover{box-shadow:0 6px 28px rgba(0,212,216,.48);transform:translateY(-1px);}

  /* HERO */
  .hero {
    min-height:100vh; padding-top:80px;
    display:flex;align-items:center;justify-content:center;
    position:relative;z-index:1;padding-left:4rem;padding-right:4rem;
  }
  .hi { max-width:1280px;width:100%; display:grid;grid-template-columns:1fr 1.12fr;gap:5rem;align-items:center; }
  .eyebrow {
    display:inline-flex;align-items:center;gap:.5rem;
    background:rgba(79,195,247,.09);border:1px solid rgba(79,195,247,.18);
    border-radius:50px;padding:.32rem .95rem;
    font-size:.7rem;font-weight:600;color:var(--teal);
    letter-spacing:.08rem;text-transform:uppercase;margin-bottom:1.3rem;
    animation:fu .8s ease both;
  }
  .ldot{width:7px;height:7px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:lp 1.2s ease infinite;}
  @keyframes lp{0%,100%{opacity:1}50%{opacity:.25}}
  .htitle{font-size:clamp(2.6rem,4.8vw,4.2rem);font-weight:800;line-height:1.1;margin-bottom:1.1rem;animation:fu .9s .1s ease both;}
  .htitle .w{color:#fff;display:block;}
  .htitle .g{
    background:linear-gradient(90deg,var(--teal2),var(--teal) 50%,var(--purple));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;
  }
  .hdesc{font-size:.95rem;font-weight:400;line-height:1.8;color:var(--dim);max-width:450px;margin-bottom:2rem;animation:fu 1s .2s ease both;}
  .hbtns{display:flex;gap:.9rem;animation:fu 1s .3s ease both;}
  .bprim{
    padding:.82rem 1.9rem;border-radius:11px;
    background:linear-gradient(135deg,var(--teal2),var(--teal));
    border:none;color:#fff;font-family:'Poppins',sans-serif;
    font-size:.88rem;font-weight:600;cursor:pointer;
    box-shadow:0 6px 28px rgba(0,212,216,.32);transition:all .3s;
  }
  .bprim:hover{transform:translateY(-2px);box-shadow:0 10px 38px rgba(0,212,216,.48);}
  .bsec{
    padding:.82rem 1.9rem;border-radius:11px;background:transparent;
    border:1px solid rgba(255,255,255,.18);color:var(--text);
    font-family:'Poppins',sans-serif;font-size:.88rem;font-weight:500;cursor:pointer;transition:all .3s;
  }
  .bsec:hover{border-color:rgba(79,195,247,.45);color:var(--teal);}
  @keyframes fu{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:translateY(0)}}

  /* DASHBOARD */
  .dash{display:grid;grid-template-columns:1fr 1fr;gap:.9rem;animation:fu 1s .4s ease both;}
  .vc{
    background:rgba(255,255,255,.05);backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:1.3rem;
    transition:all .3s;position:relative;overflow:hidden;
  }
  .vc:hover{border-color:rgba(79,195,247,.28);transform:translateY(-2px);box-shadow:0 8px 36px rgba(0,0,0,.28);}
  .vch{display:flex;align-items:center;justify-content:space-between;margin-bottom:.7rem;}
  .vct{display:flex;align-items:center;gap:.55rem;font-size:.82rem;font-weight:600;color:#fff;}
  .vi{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:.85rem;}
  .vi.t{background:rgba(0,212,216,.14);}
  .vi.p{background:rgba(240,98,146,.14);}
  .vbadge{display:flex;align-items:center;gap:.3rem;font-size:.68rem;font-weight:500;border-radius:50px;padding:.18rem .65rem;}
  .vbadge.n{background:rgba(76,175,130,.1);color:var(--green);}
  .vbadge.c{background:rgba(240,98,146,.1);color:var(--pink);}
  .vbig{font-size:2.6rem;font-weight:800;line-height:1;color:#fff;margin-bottom:.15rem;}
  .vu{font-size:.8rem;font-weight:400;opacity:.45;margin-left:.25rem;}
  .vsub{font-size:.7rem;color:var(--dim);margin-bottom:.45rem;}
  .vq{
    font-size:.7rem;font-weight:500;font-style:italic;
    color:rgba(255,255,255,.32);padding:.55rem .75rem;border-radius:8px;
    background:rgba(255,255,255,.04);border-left:2px solid var(--teal2);margin-top:.5rem;
  }
  .tc2{
    background:rgba(255,255,255,.04);backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:1.1rem;transition:all .3s;
  }
  .tc2:hover{border-color:rgba(79,195,247,.25);}
  .tch{display:flex;align-items:center;justify-content:space-between;margin-bottom:.8rem;}
  .tct{display:flex;align-items:center;gap:.45rem;font-size:.8rem;font-weight:600;color:#fff;}
  .tfoot{text-align:center;padding-top:.5rem;font-size:.72rem;color:var(--dim);}
  .tfoot span{color:var(--teal);font-weight:700;}
  .leg{display:flex;gap:1.1rem;justify-content:center;padding-top:.45rem;}
  .li{display:flex;align-items:center;gap:.35rem;font-size:.68rem;color:var(--dim);}
  .ld{width:7px;height:7px;border-radius:50%;}

  /* STATS */
  .sbar{
    padding:3.5rem 4rem;position:relative;z-index:1;
    background:rgba(79,195,247,.015);
    border-top:1px solid rgba(79,195,247,.07);
    border-bottom:1px solid rgba(79,195,247,.07);
  }
  .sinn{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);text-align:center;gap:2rem;}
  .sn{
    font-size:2.6rem;font-weight:800;display:block;
    background:linear-gradient(135deg,var(--teal2),var(--teal));
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  }
  .sl{font-size:.72rem;font-weight:500;color:var(--dim);text-transform:uppercase;letter-spacing:.1rem;margin-top:.2rem;}

  /* SECTIONS */
  .sec{padding:5.5rem 4rem;position:relative;z-index:1;max-width:1280px;margin:0 auto;}
  .slabel{
    display:inline-flex;align-items:center;gap:.45rem;
    background:rgba(79,195,247,.08);border:1px solid rgba(79,195,247,.15);
    border-radius:50px;padding:.28rem .85rem;
    font-size:.68rem;font-weight:600;color:var(--teal);
    letter-spacing:.1rem;text-transform:uppercase;margin-bottom:.9rem;
  }
  .stitle{font-size:clamp(1.9rem,3.8vw,2.9rem);font-weight:800;color:#fff;line-height:1.15;margin-bottom:.75rem;}
  .ssub{font-size:.9rem;color:var(--dim);max-width:470px;line-height:1.7;margin-bottom:3rem;}

  /* AGENT CARDS */
  .agrid{display:grid;grid-template-columns:repeat(2,1fr);gap:1.1rem;}
  .ac{
    background:rgba(255,255,255,.05);backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.08);border-radius:19px;padding:1.7rem;
    cursor:pointer;transition:all .35s;position:relative;overflow:hidden;
  }
  .ac::after{
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:var(--ac);border-radius:19px 19px 0 0;
    transform:scaleX(0);transform-origin:left;transition:transform .35s;
  }
  .ac:hover{transform:translateY(-4px);border-color:var(--aca);}
  .ac:hover::after{transform:scaleX(1);}
  .ac1{--ac:var(--teal2);--aca:rgba(0,212,216,.28);}
  .ac2{--ac:var(--green);--aca:rgba(76,175,130,.28);}
  .ac3{--ac:var(--purple);--aca:rgba(156,110,240,.28);}
  .ac4{--ac:var(--pink);--aca:rgba(240,98,146,.28);}
  .aiw{
    width:46px;height:46px;border-radius:13px;
    display:flex;align-items:center;justify-content:center;font-size:1.25rem;
    margin-bottom:1.1rem;background:rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.1);transition:all .3s;
  }
  .ac:hover .aiw{box-shadow:0 0 18px var(--ac);border-color:var(--aca);}
  .an{font-size:.95rem;font-weight:700;color:#fff;margin-bottom:.28rem;}
  .at{font-size:.7rem;font-weight:500;color:var(--ac);margin-bottom:.75rem;opacity:.85;}
  .ad{font-size:.82rem;line-height:1.65;color:var(--dim);margin-bottom:.9rem;}
  .aps{display:flex;flex-wrap:wrap;gap:.35rem;}
  .ap{font-size:.63rem;font-weight:500;padding:.22rem .7rem;border-radius:50px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.09);color:var(--dim);}

  /* HOW */
  .hgrid{display:grid;grid-template-columns:1fr 1fr;gap:5.5rem;align-items:start;}
  .steps{display:flex;flex-direction:column;gap:1.2rem;}
  .sc{
    background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
    border-radius:15px;padding:1.3rem 1.5rem;display:flex;gap:1.1rem;align-items:flex-start;transition:all .3s;
  }
  .sc:hover{border-color:rgba(79,195,247,.22);background:rgba(79,195,247,.04);}
  .snum{
    width:34px;height:34px;border-radius:9px;flex-shrink:0;
    background:linear-gradient(135deg,var(--teal2),var(--teal));
    display:flex;align-items:center;justify-content:center;
    font-size:.78rem;font-weight:700;color:#fff;box-shadow:0 4px 14px rgba(0,212,216,.28);
  }
  .stit{font-size:.88rem;font-weight:700;color:#fff;margin-bottom:.3rem;}
  .sdesc{font-size:.8rem;line-height:1.65;color:var(--dim);}
  .term{background:rgba(0,0,0,.45);border:1px solid rgba(79,195,247,.14);border-radius:15px;overflow:hidden;}
  .tbar{
    background:rgba(255,255,255,.04);padding:.75rem 1.1rem;
    display:flex;align-items:center;gap:.45rem;
    border-bottom:1px solid rgba(255,255,255,.06);
  }
  .tdot{width:10px;height:10px;border-radius:50%;}
  .tbody{padding:1.3rem 1.5rem;font-family:'Inter',monospace;font-size:.76rem;line-height:2.05;}
  .tc_{color:var(--teal2);} .tg_{color:var(--green);} .tp_{color:var(--pink);} .tw_{color:rgba(255,255,255,.7);} .td_{color:rgba(255,255,255,.32);}

  /* CTA */
  .ctaw{padding:7rem 4rem;text-align:center;position:relative;z-index:1;overflow:hidden;}
  .ctagl{
    position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
    width:850px;height:420px;
    background:radial-gradient(ellipse,rgba(79,195,247,.06) 0%,transparent 70%);pointer-events:none;
  }
  .ctat{font-size:clamp(2.4rem,4.8vw,3.8rem);font-weight:800;color:#fff;line-height:1.12;margin-bottom:.9rem;position:relative;}
  .ctat .gr2{background:linear-gradient(90deg,var(--teal2),var(--teal) 50%,var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
  .ctas{font-size:.95rem;color:var(--dim);margin-bottom:2.3rem;position:relative;}
  .ctabtns{display:flex;gap:.95rem;justify-content:center;position:relative;}
  .ctanote{margin-top:1.4rem;font-size:.7rem;color:rgba(255,255,255,.18);letter-spacing:.08rem;position:relative;}

  /* FOOTER */
  .foot{
    padding:1.8rem 4rem;border-top:1px solid rgba(255,255,255,.06);
    display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1;
  }
  .flogo{display:flex;align-items:center;gap:.55rem;font-size:.88rem;font-weight:700;color:rgba(255,255,255,.35);}
  .fcopy{font-size:.68rem;color:rgba(255,255,255,.18);}
  .flinks{display:flex;gap:1.8rem;}
  .fl{font-size:.72rem;color:rgba(255,255,255,.28);cursor:pointer;transition:color .2s;}
  .fl:hover{color:var(--teal);}

  /* REVEAL */
  .rev{opacity:0;transform:translateY(32px);transition:all .7s ease;}
  .rev.in{opacity:1;transform:translateY(0);}
`;

const genHR = () => Array.from({length:14},(_,i)=>({t:`${i*5}m`,v:72+Math.round(Math.sin(i*.9)*7+Math.random()*3)}));
const genBP = () => Array.from({length:10},(_,i)=>({t:`${i*10}m`,s:116+Math.round(Math.sin(i*.6)*5+Math.random()*3),d:76+Math.round(Math.cos(i*.6)*3+Math.random()*2)}));

const agents=[
  {cls:"ac1",icon:"🫀",name:"Health Agent",tag:"— Vital Monitor",desc:"Continuously tracks your biometrics — heart rate, BP, SpO₂, temperature. Detects anomalies instantly and alerts you before they escalate.",pills:["Real-time vitals","Anomaly alerts","AI health insights","Doctor reports"]},
  {cls:"ac2",icon:"🥗",name:"Nutrition Agent",tag:"— Meal Architect",desc:"Builds personalized weekly meal plans around your goals, allergies, and biometric data. Dynamically updates as your health evolves.",pills:["Weekly meal plans","Macro tracking","Grocery lists","Dietary filters"]},
  {cls:"ac3",icon:"⚡",name:"Exercise Agent",tag:"— Performance Coach",desc:"Designs adaptive workout programs calibrated to your fitness level, recovery state, and targets. Evolves with every single session.",pills:["Custom workouts","Recovery tracking","Progress graphs","Rest day alerts"]},
  {cls:"ac4",icon:"🧠",name:"Mental Agent",tag:"— Mind Guardian",desc:"Voice-powered journaling with emotional intelligence. Listens to your day, analyzes mood patterns, and delivers compassionate daily feedback.",pills:["Speech-to-text","Mood analysis","Daily feedback","Burnout detection"]}
];

const steps2=[
  {title:"Connect Your Data",desc:"Sync wearables, health apps, and preferences. Guardian builds your complete wellness profile in minutes."},
  {title:"AI Agents Activate",desc:"Four specialized agents begin monitoring and planning — collaborating in real-time around the clock."},
  {title:"Receive Daily Guidance",desc:"Get meal plans, workouts, alerts, and journal insights delivered through voice, chat, or dashboard."},
  {title:"Continuously Evolve",desc:"Guardian learns from your patterns, adapts recommendations, and grows smarter every single day."}
];

export default function LandingPage() {
  const [hrData]=useState(genHR);
  const [bpData]=useState(genBP);
  const [bpm,setBpm]=useState(85);
  const [vis,setVis]=useState({});
  const refs=useRef({});
  const [isAuthOpen, setIsAuthOpen] = useState(false);
   const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(()=>{
    const iv=setInterval(()=>setBpm(p=>Math.max(70,Math.min(96,p+Math.floor(Math.random()*5)-2))),1800);
    return ()=>clearInterval(iv);
  },[]);

  useEffect(()=>{
    const obs=new IntersectionObserver(entries=>entries.forEach(e=>{
      if(e.isIntersecting)setVis(v=>({...v,[e.target.dataset.id]:true}));
    }),{threshold:.12});
    Object.values(refs.current).forEach(r=>r&&obs.observe(r));
    return ()=>obs.disconnect();
  },[]);

  const r=id=>el=>{if(el){el.dataset.id=id;refs.current[id]=el;}};

  return (
    <>
      <style>{styles}</style>
      <div className="gr">
        <div className="blob b1"/><div className="blob b2"/><div className="blob b3"/>

        {/* NAV */}
        <nav className="nav">
          <div className="nlogo"><div className="nico">✦</div><span>GUAR<span>DIAN</span></span></div>
          <div className="nlinks">{["Agents","Wellness","Pricing","About"].map(l=><span key={l} className="nl">{l}</span>)}</div>
          <button className="nbtn" onClick={() => setIsAuthOpen(true)} >Get Started</button>
          
         
        </nav>
       <AuthModel
            isOpen={isAuthOpen}
            onClose={() => setIsAuthOpen(false)}
             setIsAuthenticated={setIsAuthenticated}
          />
        {/* HERO */}
        <section className="hero">
          <div className="hi">
            <div>
              <div className="eyebrow"><div className="ldot"/>AI Guardian System · Active</div>
              <h1 className="htitle">
                <span className="w">Welcome back, Alex</span>
                <span className="g">Your Guardian is On.</span>
              </h1>
              <p className="hdesc">An always-on AI companion monitoring your vitals, planning your nutrition, optimizing workouts, and nurturing your mental wellbeing — every second of every day.</p>
              <div className="hbtns">
                <button className="bprim">Activate Guardian</button>
                <button className="bsec">View Dashboard →</button>
              </div>
            </div>

            {/* LIVE DASHBOARD */}
            <div className="dash">
              {/* Heart Rate */}
              <div className="vc">
                <div className="vch">
                  <div className="vct"><div className="vi t">📈</div>Heart Rate</div>
                  <div className="vbadge n"><div className="ldot" style={{width:6,height:6}}/>Normal</div>
                </div>
                <div className="vbig">{bpm}<span className="vu">bpm</span></div>
                <div className="vsub">Status: Live</div>
                <div className="vq">"Every heartbeat is a reminder that you're alive and thriving."</div>
              </div>

              {/* Blood Pressure */}
              <div className="vc">
                <div className="vch">
                  <div className="vct"><div className="vi p">🫀</div>Blood Pressure<div className="ldot" style={{marginLeft:'.3rem'}}/></div>
                  <div className="vbadge c">↗ Check your BP!</div>
                </div>
                <div className="vbig" style={{fontSize:'2.1rem'}}>
                  120<span style={{color:'var(--dim)',fontSize:'1.3rem',margin:'0 .18rem'}}>/</span>80<span className="vu">mmHg</span>
                </div>
              </div>

              {/* HR Chart */}
              <div className="tc2">
                <div className="tch">
                  <div className="tct">Heart Rate Trend<div className="ldot"/></div>
                  <span style={{color:'var(--teal)',fontSize:'.82rem'}}>⚡</span>
                </div>
                <ResponsiveContainer width="100%" height={88}>
                  <AreaChart data={hrData} margin={{top:0,right:0,bottom:0,left:-28}}>
                    <defs>
                      <linearGradient id="hg" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4fc3f7" stopOpacity={0.28}/>
                        <stop offset="95%" stopColor="#4fc3f7" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="t" tick={{fontSize:8,fill:'rgba(255,255,255,.28)'}} tickLine={false} axisLine={false}/>
                    <YAxis tick={{fontSize:8,fill:'rgba(255,255,255,.28)'}} tickLine={false} axisLine={false} domain={['auto','auto']}/>
                    <Tooltip contentStyle={{background:'rgba(13,18,64,.92)',border:'1px solid rgba(79,195,247,.2)',borderRadius:8,fontSize:'.72rem'}} labelStyle={{color:'rgba(255,255,255,.45)'}} itemStyle={{color:'#4fc3f7'}}/>
                    <Area type="monotone" dataKey="v" stroke="#4fc3f7" strokeWidth={1.8} fill="url(#hg)" dot={false}/>
                  </AreaChart>
                </ResponsiveContainer>
                <div className="tfoot">Current BPM: <span>{bpm}</span></div>
              </div>

              {/* BP Chart */}
              <div className="tc2">
                <div className="tch">
                  <div className="tct">Blood Pressure Trend<div className="ldot"/></div>
                  <span style={{color:'var(--pink)',fontSize:'.82rem'}}>🤍</span>
                </div>
                <ResponsiveContainer width="100%" height={88}>
                  <AreaChart data={bpData} margin={{top:0,right:0,bottom:0,left:-28}}>
                    <defs>
                      <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f06292" stopOpacity={0.35}/>
                        <stop offset="95%" stopColor="#f06292" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="dg" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#9c6ef0" stopOpacity={0.28}/>
                        <stop offset="95%" stopColor="#9c6ef0" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="t" tick={{fontSize:8,fill:'rgba(255,255,255,.28)'}} tickLine={false} axisLine={false}/>
                    <YAxis tick={{fontSize:8,fill:'rgba(255,255,255,.28)'}} tickLine={false} axisLine={false} domain={[70,130]}/>
                    <Tooltip contentStyle={{background:'rgba(13,18,64,.92)',border:'1px solid rgba(240,98,146,.2)',borderRadius:8,fontSize:'.72rem'}} labelStyle={{color:'rgba(255,255,255,.45)'}}/>
                    <Area type="monotone" dataKey="s" stroke="#f06292" strokeWidth={1.8} fill="url(#sg)" dot={false} name="Systolic"/>
                    <Area type="monotone" dataKey="d" stroke="#9c6ef0" strokeWidth={1.8} fill="url(#dg)" dot={false} name="Diastolic"/>
                  </AreaChart>
                </ResponsiveContainer>
                <div className="leg">
                  <div className="li"><div className="ld" style={{background:'#f06292'}}/>Systolic</div>
                  <div className="li"><div className="ld" style={{background:'#9c6ef0'}}/>Diastolic</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* STATS */}
        <div className="sbar">
          <div className="sinn">
            {[["4","AI Agents"],["24/7","Monitoring"],["98.6%","Accuracy"],["∞","Adaptations"]].map(([n,l])=>(
              <div key={l}><span className="sn">{n}</span><div className="sl">{l}</div></div>
            ))}
          </div>
        </div>

        {/* AGENTS */}
        <div style={{maxWidth:1280,margin:'0 auto'}}>
          <section className="sec">
            <div className={`rev ${vis.ah?"in":""}`} ref={r("ah")}>
              <div className="slabel">✦ Core Agents</div>
              <h2 className="stitle">Four Guardians,<br/><span style={{background:'linear-gradient(90deg,#00d4d8,#4fc3f7,#9c6ef0)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>One Purpose.</span></h2>
              <p className="ssub">Each agent is a specialist. Together they form an integrated intelligence network watching over every dimension of your wellbeing.</p>
            </div>
            <div className="agrid">
              {agents.map((a,i)=>(
                <div key={i} className={`ac ${a.cls} rev ${vis[`ac${i}`]?"in":""}`} ref={r(`ac${i}`)} style={{transitionDelay:`${i*.09}s`}}>
                  <div className="aiw">{a.icon}</div>
                  <div className="an">{a.name}</div>
                  <div className="at">{a.tag}</div>
                  <div className="ad">{a.desc}</div>
                  <div className="aps">{a.pills.map(p=><span key={p} className="ap">{p}</span>)}</div>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* HOW IT WORKS */}
        <div style={{background:'rgba(79,195,247,.015)',borderTop:'1px solid rgba(79,195,247,.06)'}}>
          <div style={{maxWidth:1280,margin:'0 auto'}}>
            <section className="sec">
              <div className={`hgrid rev ${vis.hw?"in":""}`} ref={r("hw")}>
                <div>
                  <div className="slabel">✦ How It Works</div>
                  <h2 className="stitle">Up & Running<br/><span style={{background:'linear-gradient(90deg,#9c6ef0,#f06292)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>In Minutes.</span></h2>
                  <p className="ssub">No complex setup. No manual inputs. Guardian integrates seamlessly and begins protecting you from day one.</p>
                  <div className="term">
                    <div className="tbar">
                      <div className="tdot" style={{background:'#ff5f57'}}/><div className="tdot" style={{background:'#febc2e'}}/><div className="tdot" style={{background:'#28c840'}}/>
                      <span style={{marginLeft:'.7rem',fontSize:'.7rem',color:'rgba(255,255,255,.28)'}}>guardian_os — terminal</span>
                    </div>
                    <div className="tbody">
                      <div><span className="tc_">$</span> <span className="tw_">guardian --start --user alex</span></div>
                      <div><span className="tg_">✓</span> <span className="td_">Booting Guardian OS...</span></div>
                      <div><span className="tg_">✓</span> <span className="tw_">Health Agent: </span><span className="tg_">ONLINE</span></div>
                      <div><span className="tg_">✓</span> <span className="tw_">Nutrition Agent: </span><span className="tg_">ONLINE</span></div>
                      <div><span className="tg_">✓</span> <span className="tw_">Exercise Agent: </span><span className="tg_">ONLINE</span></div>
                      <div><span className="tg_">✓</span> <span className="tw_">Mental Agent: </span><span className="tg_">ONLINE</span></div>
                      <div><span className="tc_">⬡</span> <span className="tw_">All agents active.</span> <span style={{color:'#9c6ef0'}}>You are protected, Alex.</span></div>
                    </div>
                  </div>
                </div>
                <div className="steps">
                  {steps2.map((s,i)=>(
                    <div key={i} className="sc">
                      <div className="snum">{i+1}</div>
                      <div><div className="stit">{s.title}</div><div className="sdesc">{s.desc}</div></div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>
        </div>

        {/* CTA */}
        <section className="ctaw">
          <div className="ctagl"/>
          <div className={`rev ${vis.ct?"in":""}`} ref={r("ct")}>
            <div className="slabel" style={{margin:'0 auto 1rem',display:'inline-flex'}}>✦ Begin Today</div>
            <h2 className="ctat">Your Guardian<br/><span className="gr2">Awaits Activation.</span></h2>
            <p className="ctas">Join thousands already protected. Free 30-day trial. No credit card required.</p>
            <div className="ctabtns">
              <button className="bprim" style={{padding:'1rem 2.6rem',fontSize:'.92rem'}}>Activate Guardian</button>
              <button className="bsec"  style={{padding:'1rem 2.2rem',fontSize:'.92rem'}}>Schedule a Demo</button>
            </div>
            <p className="ctanote">AES-256 ENCRYPTED · HIPAA COMPLIANT · ZERO DATA SOLD</p>
          </div>
        </section>

        {/* FOOTER */}
        <footer className="foot">
          <div className="flogo"><div className="nico" style={{width:26,height:26,fontSize:'.72rem'}}>✦</div>GUARDIAN</div>
          <div className="fcopy">© 2025 Guardian AI Systems. All rights reserved.</div>
          <div className="flinks">{["Privacy","Terms","Contact"].map(l=><span key={l} className="fl">{l}</span>)}</div>
        </footer>
      </div>
    </>
  );
}