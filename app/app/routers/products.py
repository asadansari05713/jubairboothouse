from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query, status, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.routers.auth import get_current_admin, get_current_session
from typing import Optional, List
import os
import json
import uuid
from datetime import datetime

router = APIRouter(prefix="/products", tags=["Products"])
templates = Jinja2Templates(directory="templates")

# Product categories
CATEGORIES = ["Sports", "Casual", "Formal", "Boots", "Sneakers", "Sandals"]
SIZES = ["6", "7", "8", "9", "10", "11", "12"]
STATUSES = ["Available", "Out of Stock"]

# Ensure uploads directory exists
UPLOADS_DIR = "static/uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile) -> str:
    """Save uploaded file and return the file path"""
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1] if file.filename else '.jpg'
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOADS_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return f"/static/uploads/{unique_filename}"

@router.get("/", response_class=HTMLResponse)
async def catalog_page(
    request: Request,
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Product catalog page with search and filters"""
    query = db.query(Product)
    
    # Apply filters
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category == category)
    if status:
        query = query.filter(Product.status == status)
    
    products = query.all()
    
    return templates.TemplateResponse("catalog.html", {
        "request": request,
        "products": products,
        "categories": CATEGORIES,
        "sizes": SIZES,
        "statuses": STATUSES,
        "search": search,
        "selected_category": category,
        "selected_status": status
    })

@router.get("/detail/{product_id}", response_class=HTMLResponse)
async def product_detail(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):
    """Product detail page with image gallery and smooth animations"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get related products (same category, excluding current product)
    related_products = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()
    
    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "related_products": related_products
    })

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Admin dashboard with product management"""
    # Check if user is logged in
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    products = db.query(Product).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "products": products,
        "categories": CATEGORIES,
        "statuses": STATUSES
    })

@router.post("/admin/add")
async def add_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    product_status: str = Form("Available"),
    sizes: str = Form(""),
    image_url: str = Form(""),
    uploaded_images: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    """Add new product with multiple image uploads"""
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    # Debug: Print received form data
    print(f"DEBUG: Received form data - name: {name}, description: {description}, price: {price}, category: {category}, product_status: {product_status}, sizes: {sizes}, image_url: {image_url}")
    print(f"DEBUG: Number of uploaded images: {len(uploaded_images)}")
    
    try:
        # Save uploaded images
        uploaded_image_paths = []
        for image_file in uploaded_images:
            if image_file.filename and image_file.content_type.startswith('image/'):
                file_path = save_uploaded_file(image_file)
                uploaded_image_paths.append(file_path)
        
        # Convert uploaded image paths to JSON
        images_json = json.dumps(uploaded_image_paths) if uploaded_image_paths else None
        
        # Process sizes input
        sizes_json = None
        if sizes and sizes.strip():
            # Split by commas and/or spaces, clean up each size
            size_list = [size.strip() for size in sizes.replace(',', ' ').split() if size.strip()]
            if size_list:
                sizes_json = json.dumps(size_list)
                print(f"DEBUG: Processed sizes: {size_list} -> {sizes_json}")
            else:
                print(f"DEBUG: No valid sizes found in input: '{sizes}'")
        else:
            print(f"DEBUG: No sizes input provided or empty")
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            status=product_status,
            sizes=sizes_json,
            image_url=image_url if image_url else None,
            images=images_json
        )
        
        db.add(product)
        db.commit()
        
        print(f"DEBUG: Product added successfully with ID: {product.id}")
        print(f"DEBUG: Uploaded images: {uploaded_image_paths}")
        
    except Exception as e:
        print(f"DEBUG: Error adding product: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error adding product: {str(e)}")
    
    return RedirectResponse(url="/products/admin/dashboard", status_code=status.HTTP_302_FOUND)

@router.post("/admin/edit/{product_id}")
async def edit_product(
    request: Request,
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    product_status: str = Form(...),
    sizes: str = Form(""),
    image_url: str = Form(""),
    uploaded_images: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    """Edit product with multiple image uploads"""
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        # Save new uploaded images
        new_uploaded_image_paths = []
        for image_file in uploaded_images:
            if image_file.filename and image_file.content_type.startswith('image/'):
                file_path = save_uploaded_file(image_file)
                new_uploaded_image_paths.append(file_path)
        
        # Get existing uploaded images
        existing_images = []
        if product.images:
            try:
                existing_images = json.loads(product.images)
            except (json.JSONDecodeError, TypeError):
                existing_images = []
        
        # Combine existing and new images
        all_images = existing_images + new_uploaded_image_paths
        images_json = json.dumps(all_images) if all_images else None
        
        # Process sizes input
        sizes_json = None
        if sizes and sizes.strip():
            # Split by commas and/or spaces, clean up each size
            size_list = [size.strip() for size in sizes.replace(',', ' ').split() if size.strip()]
            if size_list:
                sizes_json = json.dumps(size_list)
                print(f"DEBUG: Processed sizes: {size_list} -> {sizes_json}")
            else:
                print(f"DEBUG: No valid sizes found in input: '{sizes}'")
        else:
            print(f"DEBUG: No sizes input provided or empty")
        
        # Update product
        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.status = product_status
        product.sizes = sizes_json
        product.image_url = image_url if image_url else None
        product.images = images_json
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")
    
    return RedirectResponse(url="/products/admin/dashboard", status_code=status.HTTP_302_FOUND)

@router.post("/admin/delete/{product_id}")
async def delete_product(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):
    """Delete product"""
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Delete uploaded image files
    if product.images:
        try:
            image_paths = json.loads(product.images)
            for image_path in image_paths:
                if image_path.startswith('/static/uploads/'):
                    file_path = image_path.replace('/static/uploads/', 'static/uploads/')
                    if os.path.exists(file_path):
                        os.remove(file_path)
        except (json.JSONDecodeError, TypeError):
            pass
    
    db.delete(product)
    db.commit()
    
    return RedirectResponse(url="/products/admin/dashboard", status_code=status.HTTP_302_FOUND)

@router.post("/admin/toggle-status/{product_id}")
async def toggle_product_status(
    request: Request,
    product_id: int,
    db: Session = Depends(get_db)
):
    """Toggle product status between Available and Out of Stock"""
    admin = get_current_admin(request, db)
    if not admin:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.status = "Out of Stock" if product.status == "Available" else "Available"
    db.commit()
    
    return RedirectResponse(url="/products/admin/dashboard", status_code=status.HTTP_302_FOUND)
