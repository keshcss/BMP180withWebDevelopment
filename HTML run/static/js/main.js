
var chart = c3.generate({
    bindto: '#chart'
    ,
    data:
    {
        columns:
        [
            ['SampleTemp', 30, 200, 100, 400, 150, 250],
            ['SamplePress', 50, 20, 10, 40, 15, 25],
            ['SampleLight', 3, 100, 200, 30, 250, 100]
        ]
        ,
        axes:
        {
            SampleLight: 'y2' // ADD
        }
    }
    ,
    axis:
    {
        y:
        {
            label:
            { // ADD
                text: 'Units',
                position: 'outer-middle'
            }
        }
        ,    
        y2:
        {
            show: true, // ADD
            label:
            { // ADD
                text: 'Units By 0.1',
                position: 'outer-middle'
            }
        }
    }
});