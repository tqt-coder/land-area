// UTE
import React from "react";

// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  CardText,
  FormGroup,
  Form,
  Row,
  Col,
} from "reactstrap";

function UserProfile() {
  return (
    <>
      <div className="content">
        <Row>
          <Col md="8">
            <Card>
              <CardHeader>
                <h5 className="title">Group Hùng + Vinh</h5>
              </CardHeader>
              <CardBody>
                <Form>
                  <Row>
                    <Col className="pr-md-1" md="5">
                      <FormGroup>
                        <label>
                          School: <h3>HCMUTE</h3>
                        </label>
                      </FormGroup>
                    </Col>
                    <Col className="px-md-1" md="3"></Col>
                    <Col className="pl-md-1" md="4"></Col>
                  </Row>
                  <Row>
                    <Col className="pr-md-1" md="6">
                      <FormGroup>
                        <label>Student 1</label>
                        <h3>Lê Nguyễn Hoàng Vinh</h3>
                      </FormGroup>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="12">
                      <FormGroup>
                        <label>Student 2</label>
                        <h3>Lê Nguyễn Hoàng Vinh</h3>
                      </FormGroup>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="pr-md-1" md="4">
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                    </Col>
                    <Col className="px-md-1" md="4"></Col>
                    <Col className="pl-md-1" md="4">
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="pl-md-1" md="4">
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                    </Col>
                  </Row>
                  <Row>
                    <Col md="8">
                      <FormGroup>
                        <p>This is final project</p>
                      </FormGroup>
                    </Col>
                  </Row>
                </Form>
              </CardBody>
              <CardFooter></CardFooter>
            </Card>
          </Col>
          <Col md="4">
            <Card className="card-user">
              <CardBody>
                <CardText />
                <div className="author">
                  <div className="block block-one" />
                  <div className="block block-two" />
                  <div className="block block-three" />
                  <div className="block block-four" />
                  <a href="#pablo" onClick={(e) => e.preventDefault()}>
                    <img
                      alt="..."
                      className="avatar"
                      src=""
                    />
                    <h4 className="title">Lecturer</h4>
                  </a>
                  <p className="description">Master</p>
                </div>
              </CardBody>
              <CardFooter>
                <div className="button-container">
                  <Button className="btn-icon btn-round" color="facebook">
                    <i className="fab fa-facebook" />
                  </Button>
                  <Button className="btn-icon btn-round" color="twitter">
                    <i className="fab fa-twitter" />
                  </Button>
                  <Button className="btn-icon btn-round" color="google">
                    <i className="fab fa-google-plus" />
                  </Button>
                </div>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default UserProfile;
