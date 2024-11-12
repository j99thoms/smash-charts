window.dccFunctions = window.dccFunctions || {};
window.dccFunctions.imageSizeMultiplier = function (value) {
    var multiplier = (0.25 * value * value) + (0.25 * value) + 0.5;
    return multiplier.toFixed(1) + 'x';
}