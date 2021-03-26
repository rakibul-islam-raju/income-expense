const searchField = document.getElementById('searchField')
const outputTable = document.querySelector('.outputTable')
const tbody = document.querySelector('.tbody')
const dataTable = document.querySelector('.dataTable')
const emptyData = document.querySelector('.emptyData')

outputTable.style.display = "none";
emptyData.style.display = "none";

const url = '/expenses/search-expenses'

searchField.addEventListener('keyup', (e)=>{
    const searchvalue = e.target.value;
    
    if(searchvalue.trim().length > 0){
        fetch(url, {
            body: JSON.stringify({searchText: searchvalue}),
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data.categories);
            console.log(data.expenses);
            
            if(data.length === 0){
                emptyData.style.display = 'block';
                emptyData.innerHTML = 'No data found.'
                dataTable.style.display = 'none';
                outputTable.style.display = 'none';
            }else{
                emptyData.style.display = 'none';
                dataTable.style.display = 'none';
                outputTable.style.display = 'block';
                (data.expenses).forEach(item => {
                    const category = (data.categories).find(obj => (obj.id == item.category_id))
                    console.log(category);

                    tbody.innerHTML = `
                        <tr>
                            <td>${ item.title }</td>
                            <td>${ item.amount }</td>
                            <td>${ item.description }</td>
                            <td>${ category.name }</td>
                            <td>${ item.date }</td>
                            <td>
                                <div class="btn-group" role="group" aria-label="Basic example">
                                    <a href="/expense/${item.id}/edit/" class="btn btn-outline-primary btn-sm">Edit</a>
                                </div>
                            </td>
                        </tr>
                    `;
                });
            }
        })
    }else{
        emptyData.style.display = 'none';
        outputTable.style.display = 'none';
        dataTable.style.display = 'block';
    }
})