const GAME_CONTROLLER_BACKGROUND_URL =
  "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?auto=format&fit=crop&w=2400&q=85";

export function CreatePageBackground() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <div
        className="absolute inset-0 bg-cover bg-center opacity-80"
        style={{ backgroundImage: `url(${GAME_CONTROLLER_BACKGROUND_URL})` }}
      />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_72%_42%,rgba(240,240,250,0.16)_0%,rgba(0,0,0,0.18)_28%,rgba(0,0,0,0.86)_72%,#000_100%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(0,0,0,0.94),rgba(0,0,0,0.72)_44%,rgba(0,0,0,0.5)_100%)]" />
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(0,0,0,0.58),rgba(0,0,0,0.18)_34%,rgba(0,0,0,0.82)_100%)]" />
    </div>
  );
}
