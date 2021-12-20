/* Handling button for sidebar appear */

$(function () {
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled").removeClass("toggled");
    });

    $("#page-content").mouseup(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled").addClass("toggled");

    });

});

/* Handling slider */

{
    let groups = Array.from(document.querySelectorAll('.multiple-range'));
    groups.forEach(group => {
        let [beginRange, endRange] = Array.from(group.querySelectorAll('input'));
        let [beginOutput, endOutput] = Array.from(group.querySelectorAll('output'));
        let min = parseFloat(beginRange.min);
        let max = parseFloat(beginRange.max);
        let step = parseFloat(beginRange.step);
        let range = max - min;
        let input = null;

        function place(event) {
            let rect = group.getBoundingClientRect();
            let x = (event instanceof MouseEvent ? event.clientX : event.touches[0].clientX) - rect.x;
            return Math.round(Math.min(max, Math.max(min, x / rect.width * range + min)) / step) * step;
        }

        function set(input, value) {
            let minDistance = parseFloat(group.dataset.minDistance) || 1;
            input.value = input === beginRange ?
                Math.min(value, parseFloat(endRange.value) - minDistance) :
                Math.max(value, parseFloat(beginRange.value) + minDistance);
            setTimeout(() => input.focus(), 0);
            update();
        }

        function update() {
            let begin = parseFloat(beginRange.value);
            let end = parseFloat(endRange.value);
            group.setAttribute('style', `
        --begin: ${(begin - min) / range * 100}%;
        --end: ${(end - min) / range * 100}%;
      `);

            beginOutput.textContent = new Function('value', `return \`${beginOutput.dataset.expression}\``)(begin);
            endOutput.textContent = new Function('value', `return \`${endOutput.dataset.expression}\``)(end);
        }

        function down(event) {
            let value = place(event);
            input = Math.abs(parseFloat(beginRange.value) - value) < Math.abs(parseFloat(endRange.value) - value) ? beginRange : endRange;
            set(input, value);
        }

        function move(event) {
            if (input) set(input, place(event));
        }

        function up(event) {
            input = null;
        }

        beginRange.addEventListener('input', event => set(beginRange, parseFloat(beginRange.value)));
        endRange.addEventListener('input', event => set(endRange, parseFloat(endRange.value)));
        group.addEventListener('mousedown', down);
        group.addEventListener('touchstart', down);
        group.addEventListener('mousemove', move);
        group.addEventListener('touchmove', move);
        group.addEventListener('mouseup', up);
        group.addEventListener('mouseout', up);
        group.addEventListener('touchendRange', up);
        group.addEventListener('touchcancel', up);
        update();

    });

}
