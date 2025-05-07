import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from utils.generate_depth_maps import generate_depth_maps
from utils.generate_sirds import generate_sirds

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DEPTH_FOLDER'] = 'static/depth_maps'
app.config['SIRDS_FOLDER'] = 'static/sirds'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DEPTH_FOLDER'], exist_ok=True)
os.makedirs(app.config['SIRDS_FOLDER'], exist_ok=True)

# Global state to store paths
state = {
    "uploaded_image": None,
    "depth_maps": [],
    "sirds_images": [],
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', 
        uploaded_image=state["uploaded_image"], 
        depth_maps=state["depth_maps"],
        sirds_images=state["sirds_images"],
        combined_image=None  # This will show the depth map or combined image
    )

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        state["uploaded_image"] = '/' + upload_path.replace('\\', '/')
        state["depth_maps"] = []
        state["sirds_images"] = []
    return redirect(url_for('index'))

@app.route('/generate_depth', methods=['POST'])
def generate_depth():
    if not state["uploaded_image"]:
        return redirect(url_for('index'))

    abs_path = state["uploaded_image"].lstrip('/')
    # Generate depth maps for the uploaded image
    depth_paths = generate_depth_maps(abs_path, app.config['DEPTH_FOLDER'])
    state["depth_maps"] = ['/' + path.replace('\\', '/') for path in depth_paths]
    return redirect(url_for('index'))

@app.route('/generate_sirds', methods=['POST'])
def generate_sirds_route():
    if not state["depth_maps"]:
        return redirect(url_for('index'))

    abs_paths = [path.lstrip('/') for path in state["depth_maps"]]
    # Generate SIRDS images from the depth maps
    sirds_paths = generate_sirds(abs_paths, app.config['SIRDS_FOLDER'])
    state["sirds_images"] = ['/' + path.replace('\\', '/') for path in sirds_paths]
    return redirect(url_for('index'))

@app.route('/combine', methods=['POST'])
def combine():
    selected = request.form.getlist('sirds')
    if len(selected) != 2:
        return redirect(url_for('index'))

    idx = int(selected[0])  # Pick the depth map corresponding to the selected SIRDS image
    combined_image = state["depth_maps"][idx]  # Just returning the selected depth map image for simplicity
    return render_template('index.html', 
        uploaded_image=state["uploaded_image"],
        depth_maps=state["depth_maps"],
        sirds_images=state["sirds_images"],
        combined_image=combined_image
    )

if __name__ == '__main__':
    app.run(debug=True)
