FROM node:22-bookworm AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY backend/ ./backend/
COPY --from=frontend /app/frontend/dist ./frontend_dist
RUN pip install --no-cache-dir -e ./backend
VOLUME ["/app/storage"]
ENV SFS_DATABASE_URL=sqlite:////app/storage/secure_files.sqlite3 SFS_STORAGE_ROOT=/app/storage
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "backend"]
