/**
 * ═══════════════════════════════════════════════════════════════════════════
 *              ALGORITHMIC ART ENGINE — ELITE 2026
 * ═══════════════════════════════════════════════════════════════════════════
 */

'use strict';

/**
 * THAM SỐ MẶC ĐỊNH (VARIABLE)
 * Có thể thay đổi tùy theo thuật toán của bạn.
 */
const DEFAULT_PARAMS = Object.freeze({
    seed: 12345,
    complexity: 1200,    // Số lượng particles
    flowScale: 0.003,    // Độ "xoáy" của noise
    speed: 2.0,          // Tốc độ di chuyển
    colorPalette: ['#6366f1', '#a5b4fc', '#4338ca', '#818cf8']
});

let params = { ...DEFAULT_PARAMS };
let particles = [];

/**
 * P5.JS SETUP
 */
function setup() {
    const canvas = createCanvas(800, 800);
    canvas.parent('canvas-wrapper');
    
    colorMode(RGB, 255, 255, 255, 255);
    pixelDensity(2); // High quality for retina displays

    initSeed(params.seed);
    initSystem();
    
    background(10, 10, 12); // Deep dark background
}

/**
 * P5.JS DRAW
 */
function draw() {
    // Tạo hiệu ứng motion trail mượt mà
    fadeBackground(20);

    for (let p of particles) {
        p.follow();
        p.update();
        p.display();
        p.edges();
    }
}

/**
 * KHỞI TẠO HỆ THỐNG (ALGORITHM SPECIFIC)
 */
function initSystem() {
    particles = [];
    for (let i = 0; i < params.complexity; i++) {
        particles.push(new Particle());
    }
}

/**
 * DỊCH CHUYỂN SEED (REPRODUCIBILITY)
 */
function initSeed(seedValue) {
    const s = parseInt(seedValue);
    randomSeed(s);
    noiseSeed(s);
    params.seed = s;
}

/**
 * REGENERATE (Khi đổi seed hoặc thay đổi lớn)
 */
function regenerate() {
    initSeed(params.seed);
    background(10, 10, 12);
    initSystem();
    loop();
}

/**
 * UI BRIDGE FUNCTIONS
 */
function updateParam(key, value) {
    params[key] = parseFloat(value);
    
    // Cập nhật text hiển thị trong UI
    const displayEl = document.getElementById(`${key}-value`);
    if (displayEl) displayEl.textContent = params[key];

    // Một số tham số cần reset lại hệ thống
    if (key === 'complexity') {
        initSystem();
    }
    
    redraw();
}

function syncUIToParams() {
    for (const [key, value] of Object.entries(params)) {
        const inputEl = document.getElementById(key);
        const displayEl = document.getElementById(`${key}-value`);
        if (inputEl) inputEl.value = value;
        if (displayEl) displayEl.textContent = value;
    }
    updateSeedDisplay();
}

/** SEED NAVIGATION */
function nextSeed() { params.seed++; regenerate(); updateSeedDisplay(); }
function prevSeed() { if(params.seed > 0) params.seed--; regenerate(); updateSeedDisplay(); }
function randomizeSeed() { params.seed = Math.floor(Math.random() * 99999); regenerate(); updateSeedDisplay(); }
function updateSeedDisplay() {
    const el = document.getElementById('seed-display');
    if (el) el.textContent = params.seed;
}

function exportImage() {
    saveCanvas(`elite-art-${params.seed}`, 'png');
}

/**
 * CORE ALGORITHM: PARTICLE CLASS
 */
class Particle {
    constructor() {
        this.pos = createVector(random(width), random(height));
        this.vel = createVector(0, 0);
        this.acc = createVector(0, 0);
        this.maxSpeed = params.speed;
        this.prevPos = this.pos.copy();
        this.color = color(params.colorPalette[Math.floor(random(params.colorPalette.length))]);
    }

    update() {
        this.vel.add(this.acc);
        this.vel.limit(this.maxSpeed);
        this.pos.add(this.vel);
        this.acc.mult(0);
    }

    follow() {
        // Flow Field logic using Perlin Noise
        let angle = noise(this.pos.x * params.flowScale, this.pos.y * params.flowScale) * TWO_PI * 4;
        let v = p5.Vector.fromAngle(angle);
        v.setMag(1);
        this.applyForce(v);
    }

    applyForce(force) {
        this.acc.add(force);
    }

    display() {
        stroke(this.color);
        strokeWeight(1.5);
        line(this.pos.x, this.pos.y, this.prevPos.x, this.prevPos.y);
        this.updatePrev();
    }

    updatePrev() {
        this.prevPos.x = this.pos.x;
        this.prevPos.y = this.pos.y;
    }

    edges() {
        if (this.pos.x > width) { this.pos.x = 0; this.updatePrev(); }
        if (this.pos.x < 0) { this.pos.x = width; this.updatePrev(); }
        if (this.pos.y > height) { this.pos.y = 0; this.updatePrev(); }
        if (this.pos.y < 0) { this.pos.y = height; this.updatePrev(); }
    }
}

/** HELPER: Fade Background */
function fadeBackground(opacity) {
    noStroke();
    fill(10, 10, 12, opacity);
    rect(0, 0, width, height);
}