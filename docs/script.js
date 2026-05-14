function add() {
  const a = Number(document.getElementById("a").value);
  const b = Number(document.getElementById("b").value);

  document.getElementById("result").innerText = `결과: ${a + b}`;
}