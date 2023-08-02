const btn = document.querySelector("#btn");
        
btn.addEventListener("click", async () => {

  try {
    const ndef = new NDEFReader();
    await ndef.scan();

    ndef.addEventListener("readingerror", () => {
      alert("error")
    });

    ndef.addEventListener("reading", ({ message, serialNumber }) => {
        alert(massage);
        alert(serialNumber)
    });
  } catch (error) {
    alert(error)
  }
});