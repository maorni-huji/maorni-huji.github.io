const MIN_MILLISECONDS_FOR_RELOAD = 10 * (10**3)
const d = (new Date()).getTime();

if ("" === document.cookie || d - parseInt(document.cookie) >= MIN_MILLISECONDS_FOR_RELOAD) {
    alert("heyy")
    document.cookie = d.toString();
    location.reload(true);
}