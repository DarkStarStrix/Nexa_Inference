const canvas = document.getElementById('backgroundCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let mouse = { x: 0, y: 0 };
let scrollY = 0;
let time = 0;

const gridSize = 70;
const nodes = [];
const lines = [];
const maxDistance = 150;

// Initialize nodes
for (let x = 0; x < canvas.width + gridSize; x += gridSize) {
  for (let y = 0; y < canvas.height + gridSize; y += gridSize) {
    const xOffset = (Math.random() - 0.5) * gridSize * 0.3;
    const yOffset = (Math.random() - 0.5) * gridSize * 0.3;
    nodes.push({
      x: x + xOffset,
      y: y + yOffset,
      baseX: x + xOffset,
      baseY: y + yOffset,
      size: Math.random() * 2 + 1,
      blink: Math.random() > 0.8,
      pulseSpeed: Math.random() * 0.02 + 0.01
    });
  }
}

// Create connections between nodes
nodes.forEach((nodeA, i) => {
  nodes.forEach((nodeB, j) => {
    if (i !== j) {
      const dx = nodeA.baseX - nodeB.baseX;
      const dy = nodeA.baseY - nodeB.baseY;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < maxDistance) {
        lines.push({
          start: nodeA,
          end: nodeB,
          distance: distance
        });
      }
    }
  });
});

// Animation function
function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Update and draw nodes
  nodes.forEach(node => {
    const dx = mouse.x - node.x;
    const dy = mouse.y - node.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const maxDist = 200;

    if (dist < maxDist) {
      const force = (maxDist - dist) / maxDist;
      node.x = node.baseX + dx * force * 0.05;
      node.y = node.baseY + dy * force * 0.05;
    } else {
      node.x += (node.baseX - node.x) * 0.05;
      node.y += (node.baseY - node.y) * 0.05;
    }
  });

  // Draw connections
  lines.forEach(line => {
    const dx = line.start.x - line.end.x;
    const dy = line.start.y - line.end.y;
    const currentDist = Math.sqrt(dx * dx + dy * dy);

    const opacity = Math.max(0, 1 - (currentDist / maxDistance));
    const timeOpacity = (Math.sin(time * line.start.pulseSpeed) + 1) * 0.2;

    ctx.beginPath();
    ctx.moveTo(line.start.x, line.start.y);
    ctx.lineTo(line.end.x, line.end.y);
    ctx.strokeStyle = `rgba(0, 255, 255, ${opacity * 0.2 + timeOpacity * 0.05})`;
    ctx.lineWidth = 0.5;
    ctx.stroke();
  });

  // Draw nodes
  nodes.forEach(node => {
    const dx = mouse.x - node.x;
    const dy = mouse.y - node.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    const brightness = dist < 200 ? (200 - dist) / 200 : 0;

    const pulse = (Math.sin(time * node.pulseSpeed) + 1) * 0.5;

    if (node.blink && Math.sin(time * 2 + node.x + node.y) > 0.8) {
      ctx.fillStyle = `rgba(255, 255, 255, ${0.7 + brightness * 0.3})`;
    } else {
      ctx.fillStyle = `rgba(0, 255, 255, ${(0.2 + pulse * 0.3) + brightness * 0.5})`;
    }

    ctx.beginPath();
    ctx.arc(node.x, node.y, node.size * (1 + pulse * 0.5), 0, Math.PI * 2);
    ctx.fill();
  });

  time += 0.01;
  requestAnimationFrame(animate);
}

// Event listeners
document.addEventListener('mousemove', (e) => {
  mouse.x = e.clientX;
  mouse.y = e.clientY;
});

window.addEventListener('scroll', () => {
  scrollY = window.scrollY;
});

window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  // Reinitialize nodes and lines
  nodes.length = 0;
  lines.length = 0;

  for (let x = 0; x < canvas.width + gridSize; x += gridSize) {
    for (let y = 0; y < canvas.height + gridSize; y += gridSize) {
      const xOffset = (Math.random() - 0.5) * gridSize * 0.3;
      const yOffset = (Math.random() - 0.5) * gridSize * 0.3;
      nodes.push({
        x: x + xOffset,
        y: y + yOffset,
        baseX: x + xOffset,
        baseY: y + yOffset,
        size: Math.random() * 2 + 1,
        blink: Math.random() > 0.8,
        pulseSpeed: Math.random() * 0.02 + 0.01
      });
    }
  }

  nodes.forEach((nodeA, i) => {
    nodes.forEach((nodeB, j) => {
      if (i !== j) {
        const dx = nodeA.baseX - nodeB.baseX;
        const dy = nodeA.baseY - nodeB.baseY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < maxDistance) {
          lines.push({
            start: nodeA,
            end: nodeB,
            distance: distance
          });
        }
      }
    });
  });
});

// Initialize animation
animate();

// Intersection Observer for sections
const sections = document.querySelectorAll('.section');
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      const cards = entry.target.querySelectorAll('.card');
      cards.forEach(card => card.classList.add('visible'));
    }
  });
}, { threshold: 0.1 });

sections.forEach(section => {
  observer.observe(section);
});

// Set active nav link
document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.navbar nav a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (currentPath.endsWith(href)) {
      link.classList.add('active');
    }
  });
});
