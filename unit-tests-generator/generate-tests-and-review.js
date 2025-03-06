import OpenAI from "openai";
const fs = require("fs");

const deepseek = new OpenAI({
  baseURL: "https://api.deepseek.com",
  apiKey: process.env.DEEPSEEK_API_KEY,
});

export async function deepseekReview() {
  const unitTest = fs.readFileSync("./__tests__/Button.test.js", "utf-8");
  const componentFile = fs.readFileSync("./src/components/Button.js", "utf-8");
  const response = await deepseek.chat.completions.create({
    messages: [
      {
        role: "system",
        content: `Please review and return a markdown if this unit tests is testing properly the 
                  file:\n\n${componentFile},
                  unit test:\n\n${unitTest}`,
      },
    ],
    model: "deepseek-chat",
  });
  const result = response.choices[0].message.content;

  fs.writeFileSync("./__tests__/testAnalysis.md", tests, "utf-8");
}
