// Дополнительные JavaScript функции
document.addEventListener('DOMContentLoaded', function() {
    // Подтверждение удаления в админке
    const deleteButtons = document.querySelectorAll('.deletelink');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот объект?')) {
                e.preventDefault();
            }
        });
    });

    // Подсветка строк таблицы
    const tableRows = document.querySelectorAll('table tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
});