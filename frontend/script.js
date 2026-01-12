const input = document.getElementById("inputText");
const list = document.getElementById("suggestions");

input.addEventListener("keyup", async () => {
    const text = input.value.trim();

    if (text.length === 0) {
        list.innerHTML = "";
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await response.json();
    list.innerHTML = "";

    data.suggestions.forEach(word => {
        const li = document.createElement("li");
        li.textContent = word;
        li.style.cursor = "pointer";

        // 🔥 CLICK EVENT
        li.addEventListener("click", () => {
            let words = input.value.split(" ");
            words[words.length - 1] = word;
            input.value = words.join(" ") + " ";
            list.innerHTML = "";
            input.focus();
        });

        list.appendChild(li);
    });
});
