if ! test -f docs/1-project-charter.md; then
  echo "❌ File 'docs/1-project-charter.md' not found"
  exit 1;
fi
echo "✅ Project charter file exists"

if grep -q "{{" docs/1-project-charter.md; then
  echo "❌ Project charter contains placeholder strings ({{ ... }})"
  exit 1;
fi
echo "✅ No leftover placeholder strings found in project charter"
