import React, { useState, useEffect, useMemo } from 'react';
import classNames from 'classnames';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { Button, ButtonGroup, Card, CardBody, CardHeader, CardTitle, Col, Row, Spinner } from 'reactstrap';
import DashBoardService from '../services/dashboardService';
import { chartExample1, chartExample4 } from 'variables/charts.js';
import { useLocation } from 'react-router-dom';

function useChartData(_code) {
    const [data, setData] = useState([]);
    const [totalArea, setTotalArea] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await DashBoardService.calcArea(_code);
                let areaSum;
                if(result){
                    areaSum = result.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
                    setTotalArea(Math.round(areaSum * 10000) / 10000);
                }
                setData(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return { data, totalArea, loading };
}

function Dashboard() {
    const [bigChartData, setBigChartData] = useState('data1');
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const selectedWard = queryParams.get('ward') || 'Label'; // Default value if not found
    const wardCode = queryParams.get('wardCode'); // Default value if not found
    const { data, totalArea, loading } = useChartData(wardCode);
    const handleBgChartData = (name) => setBigChartData(name);
    
    const pieChart = useMemo(() => ({
        labels: ["Forest_Land", "Road", "Water", "Agriculture", "Building", "Barren"],
        datasets: [{
            data: data,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    }), [data]);

    if (loading) {
        return <Spinner color="primary" />;
    }

    if (!data || !data.length || totalArea === 0) {
        return (
            <div className='content'>
                <h2 style={{ textAlign: 'center' }}>No data available to show dashboard</h2>
            </div>
        );
    }

    return (
        <>
            <div className='content'>
                <Row>
                    <Col xs='12'>
                        <Card className='card-chart'>
                            <CardHeader>
                                <Row>
                                    <Col className='text-left' sm='6'>
                                        <CardTitle tag='h2'>Land Area Statistics</CardTitle>
                                    </Col>
                                    <Col sm='6'>
                                        <ButtonGroup
                                            className='btn-group-toggle float-right'
                                            data-toggle='buttons'
                                        >
                                            <Button
                                                color='info'
                                                id='1'
                                                size='sm'
                                                tag='label'
                                                className={classNames('btn-simple', {
                                                    active: bigChartData === 'data2',
                                                })}
                                                onClick={() => handleBgChartData('data2')}
                                            >
                                                <span className='d-none d-sm-block d-md-block d-lg-block d-xl-block'>
                                                    {selectedWard}
                                                </span>
                                                <span className='d-block d-sm-none'>
                                                    <i className='tim-icons icon-gift-2' />
                                                </span>
                                            </Button>
                                        </ButtonGroup>
                                    </Col>
                                </Row>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Line
                                        data={{
                                            labels: ["Forest_Land", "Road", "Water", "Agriculture", "Building", "Barren"],
                                            datasets: [{
                                                label: selectedWard,
                                                fill: true,
                                                backgroundColor: "rgba(29,140,248,0.2)",
                                                borderColor: "#1f8ef1",
                                                borderWidth: 2,
                                                borderDash: [],
                                                borderDashOffset: 0.0,
                                                pointBackgroundColor: "#1f8ef1",
                                                pointBorderColor: "rgba(255,255,255,0)",
                                                pointHoverBackgroundColor: "#1f8ef1",
                                                pointBorderWidth: 20,
                                                pointHoverRadius: 4,
                                                pointHoverBorderWidth: 15,
                                                pointRadius: 4,
                                                data: data,
                                            }]
                                        }}
                                        options={chartExample1.options}
                                    />
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>
                <Row>
                    <Col lg='4'>
                        <Card className='card-chart'>
                            <CardHeader>
                                <h5 className='card-category'>Pie Chart</h5>
                                <CardTitle tag='h3'>
                                    <i className='tim-icons icon-bell-55 text-info' /> {totalArea} Km<sup>2</sup>
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Pie data={pieChart} />
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                    <Col lg='4'>
                        <Card className='card-chart'>
                            <CardHeader>
                                <h5 className='card-category'>Column Chart</h5>
                                <CardTitle tag='h3'>
                                    <i className='tim-icons icon-delivery-fast text-primary' /> {totalArea} Km<sup>2</sup>
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Bar
                                        data={{
                                            labels: ["Forest_Land", "Road", "Water", "Agriculture", "Building", "Barren"],
                                            datasets: [{
                                                label: selectedWard,
                                                data: data,
                                                backgroundColor: [
                                                    "rgba(255, 99, 132, 0.2)",
                                                    "rgba(54, 162, 235, 0.2)",
                                                    "rgba(255, 206, 86, 0.2)",
                                                    "rgba(75, 192, 192, 0.2)",
                                                    "rgba(153, 102, 255, 0.2)",
                                                    "rgba(255, 159, 64, 0.2)",
                                                ],
                                                borderColor: [
                                                    "rgba(255, 99, 132, 1)",
                                                    "rgba(54, 162, 235, 1)",
                                                    "rgba(255, 206, 86, 1)",
                                                    "rgba(75, 192, 192, 1)",
                                                    "rgba(153, 102, 255, 1)",
                                                    "rgba(255, 159, 64, 1)",
                                                ],
                                                borderWidth: 1,
                                            }]
                                        }}
                                    />
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                    <Col lg='4'>
                        <Card className='card-chart'>
                            <CardHeader>
                                <h5 className='card-category'>Line Chart</h5>
                                <CardTitle tag='h3'>
                                    <i className='tim-icons icon-send text-success' /> {totalArea} Km<sup>2</sup>
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Line
                                        data={{
                                            labels: ["Forest_Land", "Road", "Water", "Agriculture", "Building", "Barren"],
                                            datasets: [{
                                                label: selectedWard,
                                                fill: true,
                                                backgroundColor: "rgba(72,72,176,0.1)",
                                                hoverBackgroundColor: "rgba(72,72,176,0.1)",
                                                borderColor: "#d048b6",
                                                borderWidth: 2,
                                                borderDash: [],
                                                borderDashOffset: 0.0,
                                                data: data,
                                            }]
                                        }}
                                        options={chartExample4.options}
                                    />
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>
            </div>
        </>
    );
}

export default Dashboard;
