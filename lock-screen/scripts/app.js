const canvas = /** @type {HTMLCanvasElement} */ (
  document.getElementById("sceneCanvas")
);
const ctx = canvas.getContext("2d", { alpha: false });

const startButton = document.getElementById("startAnimation");
const recordButton = document.getElementById("recordClip");
const fallback = document.querySelector(".fallback");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

let artwork = null;
let startTime = performance.now();
let animationFrameId = null;
let recording = false;

function loadArtwork(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = `${src}?v=${Date.now()}`;
  });
}

function coverImageDimensions(img) {
  const scale = Math.max(WIDTH / img.width, HEIGHT / img.height);
  const dw = img.width * scale;
  const dh = img.height * scale;
  return {
    dx: (WIDTH - dw) / 2,
    dy: (HEIGHT - dh) / 2,
    dw,
    dh,
  };
}

function drawBackground(time) {
  const gradient = ctx.createRadialGradient(
    WIDTH / 2,
    HEIGHT * 0.2,
    WIDTH * 0.2,
    WIDTH / 2,
    HEIGHT,
    HEIGHT
  );
  gradient.addColorStop(0, "#021c29");
  gradient.addColorStop(0.45, "#03101b");
  gradient.addColorStop(1, "#00040a");

  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  // Animated aurora sweep
  const sweepY = (time * 0.05) % HEIGHT;
  const sweep = ctx.createLinearGradient(0, sweepY - 400, 0, sweepY + 400);
  sweep.addColorStop(0, "rgba(0, 150, 200, 0)");
  sweep.addColorStop(0.5, "rgba(0, 180, 255, 0.15)");
  sweep.addColorStop(1, "rgba(0, 150, 200, 0)");
  ctx.fillStyle = sweep;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
}

function drawMatrix(time) {
  ctx.save();
  ctx.globalAlpha = 0.12;
  ctx.strokeStyle = "#52f0ff";
  ctx.lineWidth = 1;

  const offsetY = (time * 60) % 48;
  for (let y = -offsetY; y < HEIGHT; y += 48) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(WIDTH, y);
    ctx.stroke();
  }

  const offsetX = (time * 30) % 36;
  for (let x = -offsetX; x < WIDTH; x += 36) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, HEIGHT);
    ctx.stroke();
  }
  ctx.restore();
}

function drawArtwork(time) {
  if (!artwork) {
    return;
  }

  const { dx, dy, dw, dh } = coverImageDimensions(artwork);

  ctx.save();
  const glowPulse = 1.04 + Math.sin(time * 0.75) * 0.08;
  ctx.filter = `brightness(${glowPulse}) contrast(1.1) saturate(1.15)`;
  ctx.drawImage(artwork, dx, dy, dw, dh);
  ctx.restore();

  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.globalAlpha = 0.32 + Math.sin(time * 2.4) * 0.12;
  ctx.shadowColor = "rgba(96,245,255,0.9)";
  ctx.shadowBlur = 45;
  ctx.drawImage(artwork, dx, dy, dw, dh);
  ctx.restore();
}

function drawScanline(time) {
  const pos = ((time * 0.18) % 1) * HEIGHT;
  const gradient = ctx.createLinearGradient(0, pos - 220, 0, pos + 220);
  gradient.addColorStop(0, "rgba(96, 255, 245, 0)");
  gradient.addColorStop(0.5, "rgba(96, 255, 245, 0.25)");
  gradient.addColorStop(1, "rgba(96, 255, 245, 0)");

  ctx.save();
  ctx.globalCompositeOperation = "screen";
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  ctx.restore();
}

function drawParticles(time) {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < 90; i += 1) {
    const seed = i * 9973;
    const speed = ((seed % 5) + 1) * 12;
    const y = ((time * speed + seed) % HEIGHT);
    const x = ((seed * 3) % WIDTH);
    const alpha = ((seed % 100) / 250) + 0.1;

    ctx.fillStyle = `rgba(96, 245, 255, ${alpha})`;
    ctx.fillRect(x, y, 2, 12);
  }
  ctx.restore();
}

function render(now) {
  const time = (now - startTime) / 1000;

  drawBackground(time);
  drawMatrix(time);
  drawArtwork(time);
  drawScanline(time);
  drawParticles(time);

  animationFrameId = requestAnimationFrame(render);
}

function restartAnimation() {
  startTime = performance.now();
  if (!animationFrameId) {
    animationFrameId = requestAnimationFrame(render);
  }
}

async function init() {
  try {
    artwork = await loadArtwork("assets/lock-subject.png");
    fallback?.classList.add("hidden");
  } catch (error) {
    console.warn("Artwork missing", error);
    fallback?.classList.remove("hidden");
  } finally {
    restartAnimation();
  }
}

startButton?.addEventListener("click", () => {
  restartAnimation();
});

recordButton?.addEventListener("click", async () => {
  if (recording) {
    return;
  }
  if (!artwork) {
    alert("Drop your image into assets/lock-subject.png first.");
    return;
  }
  if (typeof canvas.captureStream !== "function" || typeof MediaRecorder !== "function") {
    alert("Your browser does not support canvas recording. Try Chrome or Edge on desktop.");
    return;
  }

  recording = true;
  recordButton.disabled = true;
  const originalLabel = recordButton.textContent;
  recordButton.textContent = "⏺️ Recording 6s...";

  restartAnimation();

  const stream = canvas.captureStream(60);
  const options = {
    mimeType: "video/webm;codecs=vp9",
    videoBitsPerSecond: 6_000_000,
  };
  let recorder;
  try {
    recorder = new MediaRecorder(stream, options);
  } catch (err) {
    alert("Unable to start recorder in this browser.");
    recordButton.disabled = false;
    recordButton.textContent = originalLabel;
    recording = false;
    return;
  }

  const chunks = [];
  recorder.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) {
      chunks.push(event.data);
    }
  };

  recorder.onstop = () => {
    const blob = new Blob(chunks, { type: "video/webm" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "neon-lock-screen.webm";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);

    recordButton.disabled = false;
    recordButton.textContent = originalLabel;
    recording = false;
  };

  recorder.start();
  await new Promise((resolve) => setTimeout(resolve, 6000));
  recorder.stop();
});

init();
