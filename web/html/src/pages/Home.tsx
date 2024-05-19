import { Button, Col, Layout, List, Row } from "@douyinfe/semi-ui";
import { IconGithubLogo, IconMoon, IconSun } from "@douyinfe/semi-icons";
import { useState } from "react";

const ListShow = () => {
  const data = ["名称", "版本", "作者"];

  return (
    <>
      <div>
        <h3 className="titleStyle">基本信息</h3>
        <List
          dataSource={data}
          renderItem={(item) => <List.Item>{item}</List.Item>}
        />
      </div>
    </>
  );
};

function Home() {
  const [switchIcon, setswitchIcon] = useState(<IconMoon />);

  const switchMode = () => {
    const body = document.body;
    if (body.hasAttribute("theme-mode")) {
      body.removeAttribute("theme-mode");
      setswitchIcon(<IconMoon />);
    } else {
      body.setAttribute("theme-mode", "dark");
      setswitchIcon(<IconSun />);
    }
  };

  const commonStyle = {
    height: 64,
    lineHeight: "64px",
    background: "var(--semi-color-fill-0)",
  };

  const { Header, Content } = Layout;

  return (
    <>
      <Layout className="components-layout-demo">
        <Header style={commonStyle}>
          <Row type="flex" justify="end">
            <Col span={12}>
              <div className="col-content">管理界面</div>
            </Col>
            <Col span={12}>
              <div className="col-content">
                <a href="https://github.com/paopaozhi/empm" target="_blank">
                  <Button icon={<IconGithubLogo />} theme="borderless" />
                </a>
                <Button
                  icon={switchIcon}
                  onClick={switchMode}
                  theme="borderless"
                />
              </div>
            </Col>
          </Row>
        </Header>
        <Content style={{ height: 300 }}>
          <ListShow />
          {/* <Image width={360} height={200} src={demoPng} /> */}
        </Content>
        {/* <Footer style={commonStyle}>Footer</Footer> */}
      </Layout>
    </>
  );
}

export default Home;
