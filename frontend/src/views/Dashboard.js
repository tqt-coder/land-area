// UTE
import React from 'react';
// nodejs library that concatenates classes
import classNames from 'classnames';
// react plugin used to create charts
import { Bar, Line, Pie } from 'react-chartjs-2';

// reactstrap components
import { Button, ButtonGroup, Card, CardBody, CardHeader, CardTitle, Col, Row } from 'reactstrap';

// core components
import { chartExample1, chartExample2, chartExample3, chartExample4 } from 'variables/charts.js';

function Dashboard(props) {
    const [bigChartData, setbigChartData] = React.useState('data1');
    const setBgChartData = (name) => {
        setbigChartData(name);
    };
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
                                                onClick={() => setBgChartData('data2')}
                                            >
                                                <span className='d-none d-sm-block d-md-block d-lg-block d-xl-block'>
                                                    Xuan Truong village
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
                                        data={chartExample1[bigChartData]}
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
                                    <i className='tim-icons icon-bell-55 text-info' /> 2763,215 Ha
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Pie data={chartExample2} />
                                </div>
                            </CardBody>
                        </Card>
                    </Col>
                    <Col lg='4'>
                        <Card className='card-chart'>
                            <CardHeader>
                                <h5 className='card-category'>Column Chart</h5>
                                <CardTitle tag='h3'>
                                    <i className='tim-icons icon-delivery-fast text-primary' />{' '}
                                    3,5000 Ha
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Bar
                                        data={chartExample3.data}
                                        options={chartExample3.options}
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
                                    <i className='tim-icons icon-send text-success' /> 121,000 Ha
                                </CardTitle>
                            </CardHeader>
                            <CardBody>
                                <div className='chart-area'>
                                    <Line
                                        data={chartExample4.data}
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
