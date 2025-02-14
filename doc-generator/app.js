require("dotenv").config();
const fs = require("fs");
const OpenAI = require("openai");

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function docGeneratorAI(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return;
  }

  const code = fs.readFileSync(filePath, "utf-8");

  const prompt = `Analyze the following JavaScript code and generate detailed documentation in Markdown format. Include an overview, functions, classes, parameters, and usage examples:\n\n${code}`;

  try {
    const response = await openai.completions.create({
      model: "gpt-4o-mini",
      prompt: prompt,
      max_tokens: 1000,
      temperature: 0.5,
    });

    const documentation = response.choices[0].text.trim();

    const outputPath = "./DOCUMENTATION.md";
    fs.writeFileSync(outputPath, documentation, "utf-8");
    console.log(`Documentation successfully generated at: ${outputPath}`);
  } catch (error) {
    console.error("Error generating documentation with AI:", error);
  }
}

const filePath = "./example.js";
docGeneratorAI(filePath);
