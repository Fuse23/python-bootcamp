#!/bin/bash

# Находим и удаляем все папки __pycache__ внутри my_bot и её содержимое
find ./my_bot -type d -name "__pycache__" -exec rm -rf {} \;
