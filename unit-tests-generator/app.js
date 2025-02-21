const fs = require("fs");
const path = require("path");
const OpenAI = require("openai");

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

async function generateUnitTests(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    return;
  }

  const code = fs.readFileSync(filePath, "utf-8");

  const prompt = `Generate unit tests for the following React Native code using React Native Testing Library. Include tests for components, functions, and edge cases. Format the tests in a way that can be directly used in a test file:\n\n${code}`;

  try {
    const response = await openai.completions.create({
      model: "gpt-4o-mini",
      prompt: prompt,
      max_tokens: 1000,
      temperature: 0.5,
    });

    const tests = response.choices[0].text.trim();

    const testFileName = path.basename(filePath, ".js") + ".test.js";
    const testFilePath = path.join(__dirname, "__tests__", testFileName);

    if (!fs.existsSync(path.join(__dirname, "__tests__"))) {
      fs.mkdirSync(path.join(__dirname, "__tests__"));
    }

    fs.writeFileSync(testFilePath, tests, "utf-8");
    console.log(`Tests generated successfully for: ${filePath}`);
    console.log(`Test file saved at: ${testFilePath}`);
  } catch (error) {
    console.error("Error generating unit tests:", error);
  }
}

async function generateTestsForFiles(filePaths) {
  for (const filePath of filePaths) {
    await generateUnitTests(filePath);
  }
}

const filesToTest = ["./src/components/Button.js", "./src/utils/helpers.js"];

generateTestsForFiles(filesToTest);
