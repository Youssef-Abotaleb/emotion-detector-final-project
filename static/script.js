async function runEmotionDetection() {
    const text = document.getElementById("textToAnalyze").value;
    const result = document.getElementById("result");
    result.textContent = "Analyzing…";
    try {
        const response = await fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(text)}`);
        result.textContent = await response.text();
    } catch (error) {
        result.textContent = "The service could not be reached. Please try again.";
    }
}
