let assinaturaFile = null
let pdfFiles = []


// ==========================
// ASSINATURA (preview)
// ==========================
document.getElementById("assinatura").onchange = e => {

assinaturaFile = e.target.files[0]

const reader = new FileReader()

reader.onload = () => {
document.getElementById("preview").src = reader.result
}

reader.readAsDataURL(assinaturaFile)

}


// ==========================
// UPLOAD PDFs (incremental)
// ==========================
document.getElementById("pdfs").onchange = e => {

pdfFiles = [...pdfFiles, ...e.target.files]

renderPDFs()

}


// ==========================
// RENDER PDFs + LISTA
// ==========================
async function renderPDFs(){

const lista = document.getElementById("lista")
const container = document.getElementById("pdfPreviewContainer")

lista.innerHTML = ""
container.innerHTML = ""

for(let i=0;i<pdfFiles.length;i++){

const file = pdfFiles[i]

// lista com botão remover
lista.innerHTML += `
<div class="fileItem">
<span>📄 ${file.name}</span>
<button class="removeBtn" onclick="removerPDF(${i})">X</button>
</div>
`

// preview container
const div = document.createElement("div")
div.className = "pdfPreview"

const title = document.createElement("h4")
title.innerText = file.name

const canvas = document.createElement("canvas")

div.appendChild(title)
div.appendChild(canvas)
container.appendChild(div)

try{

// leitura do PDF
const buffer = await file.arrayBuffer()

const pdf = await pdfjsLib.getDocument({data: buffer}).promise
const page = await pdf.getPage(1)

// render
const viewport = page.getViewport({scale:1.5})
const ctx = canvas.getContext("2d")

canvas.height = viewport.height
canvas.width = viewport.width

await page.render({
canvasContext: ctx,
viewport: viewport
}).promise

}catch(err){
console.error("Erro ao renderizar PDF:", err)
}

}

}


// ==========================
// REMOVER PDF
// ==========================
function removerPDF(index){

pdfFiles.splice(index, 1)

renderPDFs()

}


// ==========================
// ENVIAR PARA O FLASK
// ==========================
async function enviar(){

if(!assinaturaFile || pdfFiles.length === 0){
alert("Envie assinatura e PDFs")
return
}

const formData = new FormData()

formData.append("assinatura", assinaturaFile)

pdfFiles.forEach(file=>{
formData.append("pdfs", file)
})

try{

const response = await fetch("/assinar", {
method: "POST",
body: formData
})

if(!response.ok){
throw new Error("Erro no servidor")
}

// receber ZIP
const blob = await response.blob()

const url = window.URL.createObjectURL(blob)

// download automático
const a = document.createElement("a")
a.href = url
a.download = "pdfs_assinados.zip"
document.body.appendChild(a)
a.click()
a.remove()

window.URL.revokeObjectURL(url)

}catch(error){

console.error(error)
alert("Erro ao processar PDFs")

}

}