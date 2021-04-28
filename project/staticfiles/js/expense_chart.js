const renderChart = (datas, labels) => {
  // const labels = Utils.months({count: 7});
  const data = {
    labels: labels,
    datasets: [{
      label: 'Expense',
      data: datas,
      backgroundColor: [
        // 'rgba(255, 99, 132, 0.2)',
        // 'rgba(255, 159, 64, 0.2)',
        // 'rgba(255, 205, 86, 0.2)',
        // 'rgba(75, 192, 192, 0.2)',
        'rgb(54, 162, 235)',
        // 'rgba(153, 102, 255, 0.2)',
        // 'rgba(201, 203, 207, 0.2)'
      ],
      borderColor: [
        // 'rgb(255, 99, 132)',
        // 'rgb(255, 159, 64)',
        // 'rgb(255, 205, 86)',
        // 'rgb(75, 192, 192)',
        'rgb(54, 162, 235)',
        // 'rgb(153, 102, 255)',
        // 'rgb(201, 203, 207)'
      ],
      borderWidth: 1
      }]
    };
    
    const config = {
      type: 'bar',
      data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };
    
    var myChart = new Chart(
        document.getElementById('expenseChart'),
        config
    );
}


const getChartData = () => {
    console.log('aaaaaaaaaaaaaaaaaaaaaaaa');
    fetch('/expenses/summary-data')
    .then(res => res.json())
    .then(result => {
        console.log(result)
        const category_data = result.expense_category_data
        const [data, labels] = [
          Object.values(category_data),
          Object.keys(category_data)
        ]
        console.log(data);
        renderChart(data, labels)
    })
}


document.onload = getChartData()
