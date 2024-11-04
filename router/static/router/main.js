const url_form = document.getElementById("url_form");
const submit_btn = document.getElementById("submit_btn");

url_form?.addEventListener("submit", async function (e) {
  e.preventDefault();
  submit_btn.setAttribute("disabled", true);
  let formData = new FormData(url_form);
  let contents = formData.get("original_url");

  try {
    let response = await fetch("/", {
      method: "POST",
      headers: {
        "x-Requested-with": "XMLHttpRequest",
        "Content-Type": "application/json",
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
      },
      body: JSON.stringify({
        original_url: contents,
      }),
    });

    let data = await response.json();
    console.log(data);
    console.log(response);
    if (!response.ok) {
      if (data.error == "Empty field") {
        throw new Error("Error generating short url due to empty input");
      } else {
        throw new Error("Error generating short url");
      }
    }
  } catch (error) {
    console.error(error);
  } finally {
    submit_btn.removeAttribute("disabled");
  }
});
