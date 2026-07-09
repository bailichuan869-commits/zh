const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const rootDir = path.resolve(__dirname, "..");
const courseSourceDir = path.join(rootDir, "course", "source");
const courseDistDir = path.join(rootDir, "course", "dist");
const legacyScriptPath = path.join(__dirname, "build_course_html.js");

function findSingleFileByExtension(dir, ext) {
  const files = fs.readdirSync(dir).filter(file => file.toLowerCase().endsWith(ext));
  if (files.length === 0) {
    throw new Error(`No ${ext} file found in ${dir}`);
  }
  if (files.length > 1) {
    throw new Error(`Expected one ${ext} file in ${dir}, found ${files.length}`);
  }
  return path.join(dir, files[0]);
}

function findCourseBasename() {
  return path.basename(findSingleFileByExtension(courseSourceDir, ".md"), ".md");
}

function ensureLegacyFilenames() {
  const baseName = findCourseBasename();
  const mdTarget = path.join(rootDir, `${baseName}.md`);
  const htmlTarget = path.join(rootDir, `${baseName}.html`);
  const mdSource = path.join(courseSourceDir, `${baseName}.md`);

  fs.copyFileSync(mdSource, mdTarget);
  return { baseName, mdTarget, htmlTarget };
}

function cleanupLegacyFiles(mdTarget, htmlTarget) {
  if (fs.existsSync(mdTarget)) {
    fs.unlinkSync(mdTarget);
  }
  if (fs.existsSync(htmlTarget)) {
    fs.renameSync(htmlTarget, path.join(courseDistDir, path.basename(htmlTarget)));
  }
}

function main() {
  const { mdTarget, htmlTarget } = ensureLegacyFilenames();
  try {
    execFileSync(process.execPath, [legacyScriptPath], {
      cwd: rootDir,
      stdio: "inherit"
    });
  } finally {
    cleanupLegacyFiles(mdTarget, htmlTarget);
  }
}

main();
