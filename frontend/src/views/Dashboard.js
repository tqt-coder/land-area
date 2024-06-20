import React, { useState, useEffect, useMemo } from "react";
import classNames from "classnames";
import { Bar, Line, Pie } from "react-chartjs-2";
import {
  Button,
  ButtonGroup,
  Card,
  CardBody,
  CardHeader,
  CardTitle,
  Col,
  Row,
} from "reactstrap";
import DashBoardService from "../services/dashboardService";
import { useNavigate, useLocation } from "react-router-dom";
import { chartExample1, chartExample4 } from "variables/charts.js";

import { PropagateLoader } from "react-spinners";

function useChartData(_province, _district, _ward) {
  const navigate = useNavigate();
  const [data, setData] = useState([]);
  const [imgUrl, setImgUrl] = useState([]);
  const [totalArea, setTotalArea] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await DashBoardService.calcArea(
          _province, _district, _ward,navigate
        );
        if (result && result.arr) {
          const areaSum = result.arr.reduce(
            (accumulator, currentValue) => accumulator + currentValue,
            0
          );
          setTotalArea(Math.round(areaSum * 10000) / 10000);
          setData(result.arr);
          setImgUrl(result.url);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [_province, _district, _ward, navigate]);

  return { data, totalArea, loading, imgUrl };
}

function Dashboard() {
  const [bigChartData, setBigChartData] = useState("data1");
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);

  const selectedWard = decodeURIComponent(
    queryParams.get("ward") || "Label"
  );
  const _ward = decodeURIComponent(
    queryParams.get("ward_code")
  );
  const _district = decodeURIComponent(
    queryParams.get("district_code")
  );
  const _province = decodeURIComponent(
    queryParams.get("city_code")
  );

  const { data, totalArea, loading, imgUrl } = useChartData(
    _province,
    _district,
    _ward
  );

  const handleBgChartData = (name) => setBigChartData(name);

  const pieChart = useMemo(
    () => ({
      labels: ["Background","Building", "Road", "Water","Barren","Forest_Land","Agriculture"],
      datasets: [
        {
          data: data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(89, 162, 145, 1)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
            "rgba(89, 162, 145, 1)",
          ],
          borderWidth: 1,
        },
      ],
    }),
    [data]
  );

  if (loading) {
    return (
      <div className="content">
        <div className="content__spinner">
          <PropagateLoader color="#ff3d00" size={30} />
        </div>
      </div>
    );
  }

  if (!data || !data.length || totalArea === 0) {
    return (
      <div className="content">
        <h2 style={{ textAlign: "center" }}>
          No data available to show dashboard
        </h2>
      </div>
    );
  }

  return (
    <>
      <div className="content">
        <Row>
          <Col xs="12">
            <Card className="card-chart">
              <CardHeader>
                <Row>
                  <Col className="text-left" sm="6">
                    <CardTitle tag="h2">Land Area Statistics</CardTitle>
                  </Col>
                  <Col sm="6">
                    <ButtonGroup
                      className="btn-group-toggle float-right"
                      data-toggle="buttons"
                    >
                      <Button
                        color="info"
                        id="1"
                        size="sm"
                        tag="label"
                        className={classNames("btn-simple", {
                          active: bigChartData === "data2",
                        })}
                        onClick={() => handleBgChartData("data2")}
                      >
                        <span className="d-none d-sm-block d-md-block d-lg-block d-xl-block">
                          {selectedWard}
                        </span>
                        <span className="d-block d-sm-none">
                          <i className="tim-icons icon-gift-2" />
                        </span>
                      </Button>
                    </ButtonGroup>
                  </Col>
                </Row>
              </CardHeader>
              <CardBody>
                <div className="chart-area" style={{display:"flex", justifyContent:"center", alignItems:"center"}}>
                  <img height="500px"   src={imgUrl} alt="Chart Image" />
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Pie Chart</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-bell-55 text-info" /> {totalArea}{" "}
                  Km<sup>2</sup>
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Pie data={pieChart} />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Column Chart</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-delivery-fast text-primary" />{" "}
                  {totalArea} Km<sup>2</sup>
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Bar
                    data={{
                      labels: ["Background","Building", "Road", "Water","Barren","Forest_Land","Agriculture"],
                      datasets: [
                        {
                          label: selectedWard,
                          data: data,
                          backgroundColor: [
                            "rgba(255, 99, 132, 0.2)",
                            "rgba(54, 162, 235, 0.2)",
                            "rgba(255, 206, 86, 0.2)",
                            "rgba(75, 192, 192, 0.2)",
                            "rgba(153, 102, 255, 0.2)",
                            "rgba(255, 159, 64, 0.2)",
                            "rgba(89, 162, 145, 1)",
                          ],
                          borderColor: [
                            "rgba(255, 99, 132, 1)",
                            "rgba(54, 162, 235, 1)",
                            "rgba(255, 206, 86, 1)",
                            "rgba(75, 192, 192, 1)",
                            "rgba(153, 102, 255, 1)",
                            "rgba(255, 159, 64, 1)",
                            "rgba(89, 162, 145, 1)",
                          ],
                          borderWidth: 1,
                        },
                      ],
                    }}
                  />
                </div>
              </CardBody>
            </Card>
          </Col>
          <Col lg="4">
            <Card className="card-chart">
              <CardHeader>
                <h5 className="card-category">Line Chart</h5>
                <CardTitle tag="h3">
                  <i className="tim-icons icon-send text-success" /> {totalArea}{" "}
                  Km<sup>2</sup>
                </CardTitle>
              </CardHeader>
              <CardBody>
                <div className="chart-area">
                  <Line
                    data={{
                      labels: ["Background","Building", "Road", "Water","Barren","Forest_Land","Agriculture"],
                      datasets: [
                        {
                          label: selectedWard,
                          fill: true,
                          backgroundColor: "rgba(72,72,176,0.1)",
                          hoverBackgroundColor: "rgba(72,72,176,0.1)",
                          borderColor: "#d048b6",
                          borderWidth: 2,
                          borderDash: [],
                          borderDashOffset: 0.0,
                          data: data,
                        },
                      ],
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
