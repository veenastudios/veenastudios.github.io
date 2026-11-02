// Original procedural music: no downloads, licences or network requests.
export class GameAudio {
  private context: AudioContext | null = null;
  private music: GainNode | null = null;
  private timer: number | null = null;
  private next = 0;
  private step = 0;
  private world = 'jungle';
  private active = false;
  unlock() {
    try {
      const Audio = window.AudioContext || (window as any).webkitAudioContext;
      if (!Audio) return;
      if (!this.context || this.context.state === 'closed') {
        this.context = new Audio();
        this.music = this.context!.createGain();
        this.music.gain.value = 0.12;
        this.music.connect(this.context!.destination);
      }
      void this.context!.resume().catch(() => {});
    } catch { /* Gameplay remains available without audio support. */ }
  }
  private tone(frequency: number, start: number, length: number, volume: number, type: OscillatorType, music = true) {
    const c = this.context;
    if (!c) return;
    const oscillator = c.createOscillator(), gain = c.createGain();
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, start);
    gain.gain.setValueAtTime(0, start);
    gain.gain.linearRampToValueAtTime(volume, start + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, start + length);
    oscillator.connect(gain);
    gain.connect(music && this.music ? this.music : c.destination);
    oscillator.onended = () => { oscillator.disconnect(); gain.disconnect(); };
    oscillator.start(start); oscillator.stop(start + length + 0.02);
  }
  start(world: string) {
    this.unlock();
    if (!this.context || !this.music) return;
    if (this.active && this.world === world) return;
    this.stop(); this.world = world; this.active = true; this.step = 0;
    const now = this.context.currentTime;
    this.music.gain.cancelScheduledValues(now);
    this.music.gain.setValueAtTime(0.12, now);
    this.next = now + 0.04;
    const sequences: Record<string, number[]> = {
      jungle: [0,7,12,7,3,10,15,10,5,12,17,12,3,10,7,3],
      city: [0,7,10,12,0,7,15,12,5,12,15,17,3,10,15,10],
      space: [0,12,7,19,3,15,10,22,5,17,12,24,3,15,7,19],
      water: [0,7,12,19,3,10,15,22,5,12,17,24,3,10,15,19],
      himalaya: [0,7,12,14,4,11,16,19,5,12,17,19,7,14,19,24],
    };
    const sequence = sequences[world] || sequences.jungle;
    const beat = world === 'water' ? 0.26 : world === 'city' ? 0.20 : 0.23;
    const schedule = () => {
      const c = this.context;
      if (!this.active || !c) return;
      if (this.next < c.currentTime) this.next = c.currentTime + 0.02;
      while (this.next < c.currentTime + 0.15) {
        const n = this.step % sequence.length;
        this.tone(220 * 2 ** (sequence[n] / 12), this.next, beat * 1.8, 0.36, world === 'city' ? 'triangle' : 'sine');
        if (n % 4 === 0) this.tone(110 * 2 ** ((n < 4 ? 0 : n < 8 ? 3 : n < 12 ? 5 : 3) / 12), this.next, beat * 3, 0.35, 'triangle');
        if (n % 2 === 0) this.tone(65, this.next, 0.07, 0.18, 'sine');
        this.step++; this.next += beat;
      }
    };
    schedule(); this.timer = window.setInterval(schedule, 50);
  }
  hit(danger: boolean, coin: boolean) {
    const c = this.context;
    if (!c || c.state !== 'running') return;
    const now = c.currentTime;
    if (danger) {
      if (this.music) {
        this.music.gain.cancelScheduledValues(now);
        this.music.gain.setValueAtTime(0.025, now);
        this.music.gain.linearRampToValueAtTime(0.12, now + 0.5);
      }
      this.tone(180, now, 0.16, 0.085, 'sawtooth', false);
      this.tone(110, now + 0.1, 0.22, 0.065, 'triangle', false);
    } else {
      this.tone(coin ? 880 : 660, now, 0.09, 0.075, 'sine', false);
      if (coin) this.tone(1320, now + 0.06, 0.14, 0.055, 'sine', false);
    }
  }
  stop() {
    this.active = false;
    if (this.timer !== null) window.clearInterval(this.timer);
    this.timer = null;
    if (this.context && this.music) {
      const now = this.context.currentTime;
      this.music.gain.cancelScheduledValues(now);
      this.music.gain.setTargetAtTime(0, now, 0.025);
    }
  }
  dispose() { this.stop(); const c = this.context; this.context = null; this.music = null; if (c) void c.close().catch(() => {}); }
}
