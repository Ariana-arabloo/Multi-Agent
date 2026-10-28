from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    # نام پروژه: باید رشته متنی (str) باشد و حداقل ۳ حرف داشته باشد
    name: str = Field(..., description="نام پروژه", min_length=3)
    
    # سقف بودجه: باید عدد اعشاری (float) و بزرگتر از صفر (gt=0) باشد
    budget: float = Field(..., description="سقف بودجه", gt=0)