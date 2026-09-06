const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const dataPath = path.join(root, "data", "deadlines.json");
const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));
const failures = [];

function isExternalUrl(url) {
  return /^https?:\/\//i.test(url);
}

function filePathFromUrl(url) {
  return url.split("#")[0].split("?")[0];
}

function checkLocalUrl(label, url) {
  if (!url || isExternalUrl(url)) {
    return;
  }

  const relativePath = filePathFromUrl(url);
  const absolutePath = path.join(root, relativePath);

  if (!fs.existsSync(absolutePath)) {
    failures.push(`${label}: missing ${relativePath}`);
  }
}

Object.entries(data.courses || {}).forEach(([courseKey, course]) => {
  if (course && typeof course === "object") {
    checkLocalUrl(`course ${courseKey}`, course.home);
  }
});

(data.deadlines || []).forEach((deadline) => {
  checkLocalUrl(`deadline ${deadline.id || deadline.title}`, deadline.url);
});

if (failures.length) {
  console.error("Deadline link validation failed:");
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log("Deadline link validation passed.");