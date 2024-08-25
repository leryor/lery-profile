# Convert the markdown file to docx
```bash
# Read and export .env variables
while read -r line; do export $line; done < .env

# Create output dir
mkdir -p "./build"

# Convert CVs to docx
pandoc -V phone=$MY_PHONE,email=$MY_EMAIL -f markdown -t docx ./cv/revised_cv.md -o ./build
```
