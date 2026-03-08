import io
import zipfile
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

import storage
import ai_engine

app = FastAPI(
    title="AI Practical Generator",
    description="Generate, search, and download Python practical code using Gemini AI",
    version="1.0.0"
)


# ──────────────────────────────────────────────
#  HTML Landing Page
# ──────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the browser UI."""
    import os
    html_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# ──────────────────────────────────────────────
#  List all practicals
# ──────────────────────────────────────────────
@app.get("/list")
async def list_practicals():
    """List all stored practical files."""
    practicals = storage.list_practicals()
    return {
        "count": len(practicals),
        "practicals": [
            {"filename": p["filename"], "size": p["size"]}
            for p in practicals
        ]
    }


# ──────────────────────────────────────────────
#  Download a specific file
# ──────────────────────────────────────────────
@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download a specific practical file."""
    content = storage.get_practical(filename)
    if content is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"File '{filename}' not found"}
        )
    import os
    filepath = os.path.join(storage.PRACTICALS_DIR, filename)
    return FileResponse(filepath, filename=filename, media_type="text/x-python")


# ──────────────────────────────────────────────
#  View file content (for browser)
# ──────────────────────────────────────────────
@app.get("/view/{filename}")
async def view_file(filename: str):
    """View content of a practical file."""
    content = storage.get_practical(filename)
    if content is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"File '{filename}' not found"}
        )
    return {"filename": filename, "content": content}


# ──────────────────────────────────────────────
#  MAIN ENDPOINT — Generate / Find / Update
# ──────────────────────────────────────────────
@app.post("/generate")
async def generate(aim: str = Form(...)):
    """
    The main brain endpoint.
    1. Search existing practicals for a match (AI-powered)
    2. If match found → check if updates needed → return file
    3. If no match → generate new code → save → return file
    """
    aim = aim.strip()
    if not aim:
        return JSONResponse(
            status_code=400,
            content={"error": "Aim cannot be empty"}
        )

    practicals = storage.list_practicals()

    # ── STEP 1: Try to find a matching practical ──
    matched_file = None
    if practicals:
        try:
            search_result = ai_engine.search_matching_practical(aim, practicals)
            if search_result.get("match") and search_result["match"] != "NONE":
                if search_result.get("confidence", 0) >= 0.5:
                    matched_file = search_result["match"]
        except Exception as e:
            print(f"[WARN] AI search failed, falling back to keyword: {e}")
            # Fallback to keyword search
            matched_file = storage.search_by_keyword(aim)

    # ── STEP 2: If match found, check if updates needed ──
    if matched_file:
        existing_code = storage.get_practical(matched_file)
        if existing_code:
            try:
                update_result = ai_engine.update_practical(aim, existing_code)

                if update_result.get("updated"):
                    # Save updated version with new name
                    new_filename = f"updated_{matched_file}"
                    saved_path = storage.save_practical(new_filename, update_result["code"])
                    return FileResponse(
                        saved_path,
                        filename=new_filename,
                        media_type="text/x-python",
                        headers={
                            "X-Status": "updated",
                            "X-Original": matched_file,
                            "X-Changes": update_result.get("changes", "Modified")
                        }
                    )
                else:
                    # Return existing file as-is
                    import os
                    filepath = os.path.join(storage.PRACTICALS_DIR, matched_file)
                    return FileResponse(
                        filepath,
                        filename=matched_file,
                        media_type="text/x-python",
                        headers={
                            "X-Status": "existing",
                            "X-Changes": "No changes needed"
                        }
                    )
            except Exception as e:
                print(f"[WARN] AI update failed, returning original: {e}")
                import os
                filepath = os.path.join(storage.PRACTICALS_DIR, matched_file)
                return FileResponse(
                    filepath,
                    filename=matched_file,
                    media_type="text/x-python",
                    headers={"X-Status": "existing-fallback"}
                )

    # ── STEP 3: No match → Generate new code ──
    try:
        gen_result = ai_engine.generate_practical(aim)
        files = gen_result.get("files", {})

        if not files:
            return JSONResponse(
                status_code=500,
                content={"error": "AI generated no files"}
            )

        # Save all generated files
        saved_files = []
        for filename, code in files.items():
            saved_path = storage.save_practical(filename, code)
            saved_files.append({"filename": filename, "path": saved_path})

        # Single file → direct download
        if len(saved_files) == 1:
            return FileResponse(
                saved_files[0]["path"],
                filename=saved_files[0]["filename"],
                media_type="text/x-python",
                headers={
                    "X-Status": "generated",
                    "X-Description": gen_result.get("description", "")
                }
            )

        # Multiple files → ZIP download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for sf in saved_files:
                zf.write(sf["path"], sf["filename"])
        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=practicals.zip",
                "X-Status": "generated-multiple",
                "X-File-Count": str(len(saved_files)),
                "X-Description": gen_result.get("description", "")
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Generation failed: {str(e)}"}
        )


# ──────────────────────────────────────────────
#  Delete a practical
# ──────────────────────────────────────────────
@app.delete("/delete/{filename}")
async def delete_practical(filename: str):
    """Delete a practical file."""
    if storage.delete_practical(filename):
        return {"message": f"Deleted '{filename}'"}
    return JSONResponse(
        status_code=404,
        content={"error": f"File '{filename}' not found"}
    )


# ──────────────────────────────────────────────
#  Debug endpoint — test AI without file download
# ──────────────────────────────────────────────
@app.post("/debug-generate")
async def debug_generate(aim: str = Form(...)):
    """Debug endpoint — returns JSON with full AI response details instead of file download."""
    import traceback
    import time

    aim = aim.strip()
    debug_info = {"aim": aim, "steps": []}

    # Step 1: List practicals
    practicals = storage.list_practicals()
    debug_info["practicals_count"] = len(practicals)
    debug_info["practicals"] = [p["filename"] for p in practicals]

    # Step 2: Try AI search
    if practicals:
        try:
            start = time.time()
            search_result = ai_engine.search_matching_practical(aim, practicals)
            elapsed = round(time.time() - start, 2)
            debug_info["steps"].append({
                "step": "AI Search",
                "status": "success",
                "time_seconds": elapsed,
                "result": search_result
            })
        except Exception as e:
            debug_info["steps"].append({
                "step": "AI Search",
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            })

    # Step 3: Try AI generation
    try:
        start = time.time()
        gen_result = ai_engine.generate_practical(aim)
        elapsed = round(time.time() - start, 2)
        # Truncate code for debugging display
        files_preview = {}
        for fname, code in gen_result.get("files", {}).items():
            files_preview[fname] = code[:500] + "..." if len(code) > 500 else code
        debug_info["steps"].append({
            "step": "AI Generate",
            "status": "success",
            "time_seconds": elapsed,
            "files": list(gen_result.get("files", {}).keys()),
            "description": gen_result.get("description", ""),
            "preview": files_preview
        })
    except Exception as e:
        debug_info["steps"].append({
            "step": "AI Generate",
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

    return JSONResponse(content=debug_info)


# ──────────────────────────────────────────────
#  Health check
# ──────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "message": "AI Practical Generator is running 🚀"}
