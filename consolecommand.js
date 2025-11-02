let lastEight = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,999999999]
let k = 0;

(async () => {
  const links = new Set();
  // Initial loop
  document.querySelectorAll('img[src*="/media/"]').forEach(img => links.add(`${img.src}`));

  // Loop stops when the last 8 cycles dont change in link size
  for (let i = 0; lastEight.reduce((acc,curr) => acc+curr,0)/20!=lastEight[19]; i++) {
    k==19 ? k = 0 : k++
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 1500));
    document.querySelectorAll('img[src*="/media/"]').forEach(img => links.add(`${img.src}`));
    console.log(`Pass ${i + 1}: ${links.size} links so far`);
    lastEight[k] = links.size
  }

  // Create text file from collected links
  const blob = new Blob([...links].join('\n').split(), { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'bookmarks.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  console.log(`✅ Saved ${links.size} tweet links to bookmarks.txt`);
})();