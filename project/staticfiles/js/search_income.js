const searchField = document.getElementById('searchField')
const outputTable = document.querySelector('.outputTable')
const tbody = document.querySelector('.tbody')
const dataTable = document.querySelector('.dataTable')
const emptyData = document.querySelector('.emptyData')
const loding = document.querySelector('.loding')

outputTable.style.display = "none";
emptyData.style.display = "none";
loding.style.display = "none";

const url = '/income/search-income'

searchField.addEventListener('keyup', (e)=>{
    const searchvalue = e.target.value;
    
    if(searchvalue.trim().length > 0){
        loding.style.display = "block";
        tbody.innerHTML = ''
        fetch(url, {
            body: JSON.stringify({searchText: searchvalue}),
            method: 'POST'
        })
        .then(res => res.json())
        .then(data => {
            loding.style.display = "none";
            if(data.length === 0){
                emptyData.style.display = 'block';
                emptyData.innerHTML = 'No data found.'
                dataTable.style.display = 'none';
                outputTable.style.display = 'none';
            }else{
                emptyData.style.display = 'none';
                dataTable.style.display = 'none';
                outputTable.style.display = 'block';
                (data.incomes).forEach(item => {
                    const source = (data.sources).find(obj => (obj.id == item.source_id))
                    console.log(source);

                    tbody.innerHTML += `
                        <tr>
                            <td>${ item.title }</td>
                            <td>${ item.amount }</td>
                            <td>${ item.description }</td>
                            <td>${ source.name }</td>
                            <td>${ item.date }</td>
                            <td>
                                <div class="btn-group" role="group" aria-label="Basic example">
                                    <a href="/income/${item.id}/edit/" class="btn btn-outline-primary btn-sm">Edit</a>
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