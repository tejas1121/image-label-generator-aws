const API_BASE =
  "https://wm6ru7j2s2.execute-api.us-east-1.amazonaws.com/prod";

const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const preview = document.getElementById("preview");
const previewSection = document.getElementById("previewSection");
const statusEl = document.getElementById("status");
const labelsEl = document.getElementById("labels");
const errorEl = document.getElementById("error");

let selectedFile = null;

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0];
  if (!selectedFile) return;

  uploadBtn.disabled = false;
  labelsEl.innerHTML = "";
  errorEl.textContent = "";

  preview.innerHTML = "";
  const img = document.createElement("img");
  img.src = URL.createObjectURL(selectedFile);
  preview.appendChild(img);

  previewSection.style.display = "block";
  statusEl.textContent = "Ready to analyze image";
});

uploadBtn.addEventListener("click", uploadImage);

async function uploadImage() {
  uploadBtn.disabled = true;
  statusEl.textContent = "Generating secure upload URL...";

  try {
    const res = await fetch(
      `${API_BASE}/upload-url?file_name=${encodeURIComponent(
        selectedFile.name
      )}`
    );

    const { upload_url, image_name } = await res.json();
    if (!upload_url) throw new Error("Upload URL error");

    statusEl.textContent = "Uploading image to cloud...";

    await fetch(upload_url, {
      method: "PUT",
      headers: { "Content-Type": selectedFile.type },
      body: selectedFile,
    });

    statusEl.textContent = "Analyzing image with AI...";
    pollLabels(image_name);
  } catch (err) {
    errorEl.textContent = err.message;
    uploadBtn.disabled = false;
  }
}

async function pollLabels(imageName) {
  for (let i = 0; i < 10; i++) {
    await new Promise((r) => setTimeout(r, 3000));

    const res = await fetch(
      `${API_BASE}/labels?image_name=${encodeURIComponent(imageName)}`
    );

    if (res.status === 200) {
      const data = await res.json();
      renderLabels(data.Labels);
      statusEl.textContent = "Analysis complete";
      uploadBtn.disabled = false;
      return;
    }
  }

  errorEl.textContent = "Analysis timed out";
  uploadBtn.disabled = false;
}

function renderLabels(labels) {
  labelsEl.innerHTML = "";

  labels.forEach((l) => {
    const card = document.createElement("div");
    card.className = "label-card";

    const name = document.createElement("div");
    name.className = "label-name";
    name.textContent = l.Name;

    const bar = document.createElement("div");
    bar.className = "confidence-bar";

    const fill = document.createElement("div");
    fill.className = "confidence-fill";
    fill.style.width = `${Number(l.Confidence).toFixed(1)}%`;

    bar.appendChild(fill);

    card.appendChild(name);
    card.appendChild(bar);
    labelsEl.appendChild(card);
  });
}
