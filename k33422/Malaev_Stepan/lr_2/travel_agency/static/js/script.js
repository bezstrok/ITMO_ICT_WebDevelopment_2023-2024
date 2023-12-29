"use strict";

const words = [
    "journey through the Amazon Rainforest",
    "cultural exploration in Kyoto",
    "historical quest to the Pyramids of Giza",
    "culinary adventure to Tuscany",
    "wine tasting in Napa Valley",
    "art tour in the Louvre, Paris",
    "diving trip to the Great Barrier Reef",
    "pilgrimage to Santiago de Compostela",
    "wildlife expedition in the Galapagos Islands",
    "ski escape to the Alps",
]; // TODO: Take names from db

function typeEffect(dynamicText, wordIndex = 0, charIndex = 0, isDeleting = false) {
    const typingSpeed = 80;
    const deletingSpeed = 100;
    const delayBetweenWords = 1500;

    const currentWord = words[wordIndex];
    dynamicText.textContent = currentWord.substring(0, charIndex);
    dynamicText.classList.toggle("stop-blinking", isDeleting);

    if (!isDeleting && charIndex < currentWord.length) {
        charIndex++;
        setTimeout(() => typeEffect(dynamicText, wordIndex, charIndex, isDeleting), typingSpeed);
    } else if (isDeleting && charIndex > 0) {
        charIndex--;
        setTimeout(() => typeEffect(dynamicText, wordIndex, charIndex, isDeleting), deletingSpeed);
    } else {
        isDeleting = !isDeleting;
        dynamicText.classList.remove("stop-blinking");
        wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
        setTimeout(() => typeEffect(dynamicText, wordIndex, charIndex, isDeleting), delayBetweenWords);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    $('.dropdown-trigger').dropdown();
    const dynamicText = document.querySelector("h2 span");
    typeEffect(dynamicText);
});
