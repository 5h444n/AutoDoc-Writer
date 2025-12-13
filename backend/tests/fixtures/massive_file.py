python3 -c "with open('backend/tests/fixtures/massive_file.py', 'w') as f:
    f.write('def huge_process():\n');
    f.write('\n'.join([f'    x_{i} = {i} * {i}' for i in range(600)]));
    f.write('\n    return x_599')"