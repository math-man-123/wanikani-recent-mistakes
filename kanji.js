function createKanjiLinks() {
  let links = document.querySelector('.links');
  let characters = '{{similar_characters}}'.split(', ');
  let meanings = '{{similar_meanings}}'.split(', ');

  function createKanjiLink(character, meaning) {
    let kanji = document.createElement('a');
    kanji.href = `https://www.wanikani.com/kanji/${character}`;
    kanji.classList.add('kanji');

    kanji.innerHTML = `
		<div class="character">${character}</div>
		<div class="meaning">${meaning}</div>
		`.trim();

    return kanji;
  }

  for (let i = 0; i < characters.length; i++) {
    let kanjiLink = createKanjiLink(characters[i], meanings[i]);
    links.appendChild(kanjiLink);
  }
}

function deleteEmptyParts() {
  let onyomi = document.getElementById('onyomi');
  let kunyomi = document.getElementById('kunyomi');

  function deleteRowIfEmpty(row) {
    let primary = row.querySelector('.primary').innerHTML;
    let other = row.querySelector('.other').innerHTML;

    if (!primary && !other) row.remove();
  }

  deleteRowIfEmpty(onyomi);
  deleteRowIfEmpty(kunyomi);

  let similar = document.getElementById('similar');
  let rulers = document.querySelectorAll('hr');
  let lastRuler = rulers[rulers.length - 1];

  if (!'{{similar_characters}}') {
    similar.remove();
    lastRuler.remove();
  }
}

createKanjiLinks();
deleteEmptyParts();
