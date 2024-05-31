export const eel = window.eel

// Expose the `sayHelloJS` function to Python as `say_hello_js`
function sayHelloJS(x) {
  console.log( 'Hello from ' + x )
}
// WARN: must use window.eel to keep parse-able eel.expose{...}
window.eel.expose( sayHelloJS, 'sayHelloJS' )

function hello(x) {
  console.log(x);
}
window.eel.expose(hello, 'hello');