// UTE
import React from "react";

// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  FormGroup,
  Form,
  Row,
  Col,
} from "reactstrap";

function NewsPage() {
  return (
    <>
      <div className="content">
        <Row>
          <Col md="12">
            <Card>
              <CardHeader>
                <h5 className="title-t">Bản tin</h5>
              </CardHeader>
              <CardBody>
                <Form>
                  <Row>
                    <Col className="m-lg-1" md="6">
                      <FormGroup>
                        <h4>Việc sử dụng các mô hình tính diện tích đất trong lĩnh vực đất đai mang lại nhiều lợi ích quan trọng cho đời sống xã hội:</h4>
                      </FormGroup>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="m-lg-1" md="12">
                    <h5>1. Quy hoạch và phát triển đô thị</h5>
                      <ul className="m-lg-4">
                        <li>Phát triển cơ sở hạ tầng: Hỗ trợ việc lập kế hoạch và xây dựng các cơ sở hạ tầng như đường sá, cầu cống, và hệ thống cấp thoát nước một cách hiệu quả.</li>
                      </ul>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="m-lg-1" md="12">
                    <h5>2. Quản lý và bảo vệ tài nguyên đất:</h5>
                      <ul className="m-lg-4">
                        <li>Bảo vệ môi trường: Giúp giám sát và bảo vệ các khu vực đất nhạy cảm về môi trường, ngăn ngừa sự xâm hại và sử dụng không bền vững.</li>
                      </ul>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="m-lg-1" md="12">
                    <h5>3. Phát triển nông nghiệp:</h5>
                      <ul className="m-lg-4">
                        <li>Tối ưu hóa canh tác: Giúp nông dân và các nhà quản lý nông nghiệp tính toán và phân chia đất canh tác hợp lý, tăng năng suất và hiệu quả sản xuất.</li>
                        <li>Quản lý thủy lợi: Hỗ trợ lập kế hoạch và xây dựng các hệ thống tưới tiêu, thoát nước hiệu quả.</li>
                      </ul>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="m-lg-1" md="12">
                    <h5>4. Phát triển bất động sản:</h5>
                      <ul className="m-lg-4">
                        <li>Đánh giá giá trị đất: Giúp các nhà đầu tư và phát triển bất động sản đánh giá chính xác giá trị của các khu đất, lập kế hoạch phát triển và kinh doanh hiệu quả.</li>
                        <li>Thiết kế và xây dựng: Hỗ trợ việc thiết kế và xây dựng các dự án bất động sản phù hợp với quy hoạch và sử dụng đất đai hợp lý.</li>
                      </ul>
                    </Col>
                  </Row>
                  <Row>
                    <Col className="m-lg-1" md="12">
                    <h5>5. Cải thiện quản lý hành chính và pháp lý:</h5>
                      <ul className="m-lg-4">
                        <li>Quản lý dữ liệu đất đai: Tạo ra và quản lý các bản đồ, dữ liệu đất đai một cách hệ thống và dễ dàng truy cập, hỗ trợ công tác quản lý hành chính.</li>
                        <li>Thủ tục pháp lý: Giúp đơn giản hóa và minh bạch hóa các thủ tục pháp lý liên quan đến quyền sở hữu và chuyển nhượng đất đai.</li>
                      </ul>
                    </Col>
                  </Row>
                </Form>
              </CardBody>
              <CardFooter></CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default NewsPage;
