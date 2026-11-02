import { useEffect, useRef, useState } from 'react';

type Target = {
  id: number;
  x: number;
  born: number;
  duration: number;
  danger: boolean;
  glyph: string;
  size: number;
};
type Burst = {
  id: number;
  x: number;
  y: number;
  danger: boolean;
  text: string;
};
type Phase = 'hub' | 'play' | 'over';
const SAFE = ['⭐', '💎', '🍭', '⚡', '🎯'];
const COIN = '🪙';
const DANGER = ['😈', '💣'];
const games = [
  {
    id: 'tap-rush',
    name: 'TAP RUSH',
    live: true,
    tag: 'Tap • Dodge • Score Big!',
  },
];

function sprite(t: Target) {
  if (t.danger) return t.glyph === '💣' ? 5 : 4;
  if (t.glyph === COIN) return 3;
  return t.glyph === '💎' ? 1 : t.glyph === '🍭' || t.glyph === '🎯' ? 2 : 0;
}
function App() {
  const [bursts, setBursts] = useState<Burst[]>([]);
  const burstId = useRef(0);
  const burstTimers = useRef<number[]>([]);
  useEffect(() => () => burstTimers.current.forEach(clearTimeout), []);
  const burst = (t: Target, e: React.PointerEvent<HTMLButtonElement>) => {
    const root = e.currentTarget.closest('main')!.getBoundingClientRect();
    const rect = e.currentTarget.getBoundingClientRect();
    const id = ++burstId.current;
    setBursts(old => [
      ...old.slice(-5),
      {
        id,
        x: rect.left - root.left + rect.width / 2,
        y: rect.top - root.top + rect.height / 2,
        danger: t.danger,
        text: t.danger ? '−2' : t.glyph === COIN || combo >= 4 ? '+2' : '+1',
      },
    ]);
    burstTimers.current.push(
      window.setTimeout(
        () => setBursts(old => old.filter(b => b.id !== id)),
        650
      )
    );
  };
  const [phase, setPhase] = useState<Phase>('hub');
  const [score, setScore] = useState(0);
  const [best, setBest] = useState(() =>
    Number(localStorage.getItem('tapRushBest') || 0)
  );
  const [coins, setCoins] = useState(() =>
    Number(localStorage.getItem('srCoins') || 0)
  );
  const [time, setTime] = useState(30);
  const [targets, setTargets] = useState<Target[]>([]);
  const [combo, setCombo] = useState(0);
  const [flash, setFlash] = useState('');
  const [settings, setSettings] = useState(false);
  const [sound, setSound] = useState(
    () => localStorage.getItem('srSound') !== 'off'
  );
  const startRef = useRef(0);
  const idRef = useRef(1);
  const flashTimer = useRef<number | null>(null);
  const begin = () => {
    setBursts([]);
    setScore(0);
    setTime(30);
    setTargets([]);
    setCombo(0);
    setFlash('');
    startRef.current = performance.now();
    setPhase('play');
  };
  const home = () => {
    setPhase('hub');
    setTargets([]);
  };
  useEffect(() => {
    localStorage.setItem('srSound', sound ? 'on' : 'off');
  }, [sound]);
  useEffect(() => {
    if (phase !== 'play') return;
    let raf = 0,
      lastSpawn = 0;
    const loop = (now: number) => {
      const elapsed = (now - startRef.current) / 1000,
        left = Math.max(0, 30 - elapsed);
      setTime(Math.ceil(left));
      if (left <= 0) {
        setPhase('over');
        setTargets([]);
        setScore(final => {
          setBest(old => {
            const next = Math.max(old, final);
            localStorage.setItem('tapRushBest', String(next));
            return next;
          });
          return final;
        });
        return;
      }
      const progress = elapsed / 30,
        endRush = progress > 0.7 ? (progress - 0.7) / 0.3 : 0,
        spawnGap = 900 - progress * 390 - endRush * 150;
      if (now - lastSpawn > spawnGap) {
        lastSpawn = now;
        const roll = Math.random(),
          burst =
            endRush > 0.35
              ? roll < 0.45 + endRush * 0.25
                ? 3
                : 2
              : roll < 0.06 + endRush * 0.12
                ? 3
                : roll < 0.24 + progress * 0.2
                  ? 2
                  : 1;
        setTargets(old => {
          const fresh: Target[] = [];
          const split = endRush > 0.35 && burst >= 2,
            pair = endRush > 0.2 && Math.random() < 0.24;
          for (let i = 0; i < burst; i++) {
            const pairedCoin = pair && i === 0,
              pairedDanger = pair && i === 1,
              danger = pairedDanger || (!pairedCoin && Math.random() < 0.22),
              coin = pairedCoin || (!danger && Math.random() < 0.16);
            fresh.push({
              id: idRef.current++,
              x:
                split && i < 2
                  ? i === 0
                    ? 8 + Math.random() * 25
                    : 58 + Math.random() * 25
                  : 8 + Math.random() * 78,
              born: now + (split && i < 2 ? 0 : i * 70),
              duration: 5200 - progress * 2100 - endRush * 650,
              danger,
              glyph: danger
                ? DANGER[Math.floor(Math.random() * DANGER.length)]
                : coin
                  ? COIN
                  : SAFE[Math.floor(Math.random() * SAFE.length)],
              size: 58 + Math.random() * 18,
            });
          }
          return [...old, ...fresh].slice(-11);
        });
      }
      setTargets(old => old.filter(t => now - t.born < t.duration + 250));
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [phase]);
  const hit = (t: Target) => {
    if (phase !== 'play') return;
    setTargets(v => v.filter(x => x.id !== t.id));
    if (t.danger) {
      setScore(v => Math.max(0, v - 2));
      setCombo(0);
      setFlash('DANGER −2');
      navigator.vibrate?.([70, 35, 70]);
    } else {
      const next = combo + 1,
        isCoin = t.glyph === COIN;
      setCombo(next);
      setScore(v => v + (isCoin ? 2 : 1) + (next >= 5 ? 1 : 0));
      setFlash(isCoin ? 'COIN +2!' : next >= 5 ? 'COMBO +2!' : '+1');
      if (isCoin)
        setCoins(v => {
          const n = v + 1;
          localStorage.setItem('srCoins', String(n));
          return n;
        });
      navigator.vibrate?.(25);
    }
    if (sound && 'AudioContext' in window) {
      const C = window.AudioContext || (window as any).webkitAudioContext;
      const c = new C(),
        o = c.createOscillator(),
        g = c.createGain();
      o.frequency.value = t.danger ? 120 : 520;
      g.gain.value = 0.035;
      o.connect(g);
      g.connect(c.destination);
      o.start();
      o.stop(c.currentTime + 0.06);
    }
    if (flashTimer.current) clearTimeout(flashTimer.current);
    flashTimer.current = window.setTimeout(() => setFlash(''), 420);
  };
  if (phase === 'hub')
    return (
      <main className="hub">
        <img
          className="premiumHome"
          src="https://veenastudios.in/file_00000000c1108207931406ed369edda6.jpg?v=2"
          alt="SR Gamers Kids"
        />
        <div className="language">SR GAMERS · GAME 01</div>
        <div className="coinBox" aria-label={'Coins: ' + coins}>
          🪙 {coins}
        </div>
        <button
          className="gear"
          aria-label="Settings"
          onClick={() => setSettings(true)}
        >
          ⚙️
        </button>
        <section className="liveShelf">
          <h2>PLAY GAMES</h2>
          {games
            .filter(g => g.live)
            .map(g => (
              <button key={g.id} className="gameCard" onClick={begin}>
                <span>
                  <img
                    src="https://tap-rush-trial-2-acshom.v2.appdeploy.ai/tap-rush-3d.png"
                    style={{ borderRadius: 18 }}
                    alt=""
                  />
                </span>
                <b>{g.name}</b>
                <small>{g.tag}</small>
                <em>▶ PLAY</em>
              </button>
            ))}
        </section>
        <p className="collectionNote">SR GAMERS • GAME 01</p>
        {settings && (
          <div className="modal">
            <button
              className="close"
              aria-label="Close settings"
              onClick={() => setSettings(false)}
            >
              ✕
            </button>
            <h2>SETTINGS</h2>
            <button className="setting" onClick={() => setSound(v => !v)}>
              🔊 Sound <b>{sound ? 'ON' : 'OFF'}</b>
            </button>
            <p>
              More games will appear here automatically as the SR GAMERS
              collection grows.
            </p>
            <div className="best">
              🏆 Best Tap Rush: <b>{best}</b>
            </div>
          </div>
        )}
      </main>
    );
  return (
    <main
      className={
        'game jungleGame ' +
        (time <= 10 && phase === 'play' ? 'finalRush ' : '') +
        (flash.includes('DANGER') ? 'dangerFlash' : '')
      }
    >
      <div className="jungleMist" aria-hidden="true" />
      <header>
        <div>
          <small>SCORE</small>
          <strong>{score}</strong>
        </div>
        <div className="brand">
          TAP
          <br />
          <b>RUSH</b>
        </div>
        <div>
          <small>TIME</small>
          <strong>{time}</strong>
        </div>
      </header>
      {phase === 'play' && (
        <>
          <div className="roundTrack" aria-hidden="true">
            <i style={{ width: (time / 30) * 100 + '%' }} />
          </div>
          <div className="jungleGuide" aria-hidden="true">
            <img
              src="https://tap-rush-trial-2-acshom.v2.appdeploy.ai/tap-rush-3d.png"
              alt=""
            />
            <span>
              {flash.includes('DANGER')
                ? 'Careful!'
                : combo >= 5
                  ? 'Great streak!'
                  : time <= 10
                    ? 'Final rush!'
                    : 'Tap the treasures'}
            </span>
          </div>
          <div className="combo">
            {combo >= 3 ? '🔥 ' + combo + ' COMBO' : ''}
          </div>
          <div className="lane">
            {targets.map(t => (
              <button
                aria-label={t.danger ? 'danger target' : 'safe target'}
                key={t.id}
                onPointerDown={e => {
                  burst(t, e);
                  hit(t);
                }}
                className={'target ' + (t.danger ? 'bad' : 'good')}
                style={{
                  left: `min(${t.x}%, calc(100% - ${t.size}px - 8px))`,
                  width: t.size,
                  height: t.size,
                  animationDuration: t.duration + 'ms',
                  animationDelay:
                    Math.max(0, t.born - performance.now()) + 'ms',
                }}
              >
                <span
                  className={'sprite sprite-' + sprite(t)}
                  aria-hidden="true"
                />
              </button>
            ))}
          </div>
          {bursts.map(b => (
            <div
              key={b.id}
              className={'tapBurst ' + (b.danger ? 'hurt' : '')}
              style={{ left: b.x, top: b.y }}
              aria-hidden="true"
            >
              <b>{b.text}</b>
              {Array.from({ length: 7 }, (_, i) => (
                <i
                  key={i}
                  style={
                    {
                      '--dx': Math.cos((i * Math.PI * 2) / 7) * 48 + 'px',
                      '--dy': Math.sin((i * Math.PI * 2) / 7) * 48 + 'px',
                    } as React.CSSProperties
                  }
                />
              ))}
            </div>
          ))}
          {flash && (
            <div className={'flash ' + (flash.includes('DANGER') ? 'red' : '')}>
              {flash}
            </div>
          )}
        </>
      )}
      {phase === 'over' && (
        <section className="panel">
          <div className="resultCrown" aria-hidden="true">
            ✦
          </div>
          <div className="mascot">🏆</div>
          <h1>{score}</h1>
          <p>Final score • Best {best}</p>
          <button onClick={begin}>PLAY AGAIN</button>
          <button className="homeBtn" onClick={home}>
            ⌂ SR GAMERS HOME
          </button>
          <a className="exploreVeena" href="https://veenastudios.in/" target="_blank" rel="noopener noreferrer">Explore Veena Studios ↗<small>More games · Books · Stories</small></a>
        </section>
      )}
      <footer>SR GAMERS • TAP RUSH</footer>
    </main>
  );
}
export default App;

