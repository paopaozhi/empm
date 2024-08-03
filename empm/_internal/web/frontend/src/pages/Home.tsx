import {
  Button,
  ButtonGroup,
  Col,
  Descriptions,
  Layout,
  List,
  Row,
} from "@douyinfe/semi-ui";
import { IconGithubLogo, IconMoon, IconSun } from "@douyinfe/semi-icons";
import { useEffect, useState } from "react";
import "./Home.css";

function ListShow({
  titleName,
  data,
  renderType,
}: {
  titleName: string;
  data: any;
  renderType: boolean;
}) {
  const ListRenderType = (item: any) => {
    if (renderType) {
      return (
        <Row>
          <Col span={12}>
            <div className="col-list">{item[0]}</div>
          </Col>
          <Col span={12}>
            <div className="col-list">{item[1]}</div>
          </Col>
        </Row>
      );
    } else {
      return (
        <List.Item
          main={
            <div>
              <Descriptions
                align="center"
                size="small"
                row
                data={[
                  { key: "名称", value: item.name },
                  { key: "版本", value: item.version },
                  { key: "链接", value: item.url },
                ]}
              />
            </div>
          }
          extra={
            <ButtonGroup theme="borderless">
              <Button>修改</Button>
              <Button>删除</Button>
            </ButtonGroup>
          }
        />
      );
    }
  };

  return (
    <div>
      <h3 className="titleStyle">{titleName}</h3>
      <List dataSource={data} renderItem={ListRenderType} />
    </div>
  );
}

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

  // const myMap = [
  //   ["名称", "模板工程"],
  //   ["版本", "0.0.7"],
  //   ["作者", "paopaozhi"],
  // ];

  // const pack_info = {
  //   name: "empm",
  //   version: "0.1.0",
  //   authors: ["paopaozhi"],
  // };

  const [pack_dependencies, setPack_dependencies] = useState([]);
  const [pack_info, setPack_info] = useState<string | unknown>(0);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/pack/info")
      .then((repoonse) => repoonse.json())
      .then((data) => {
        setPack_info(Object.entries(data));
      });

    fetch("http://127.0.0.1:5000/pack/dependencies")
      .then((response) => response.json())
      .then((data) => {
        setPack_dependencies(data);
      });
  }, []);

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
          <ListShow titleName="基本信息" data={pack_info} renderType />
          <ListShow
            titleName="已安装的包"
            data={pack_dependencies}
            renderType={false}
          />
        </Content>
        {/* <Footer style={commonStyle}>Footer</Footer> */}
      </Layout>
    </>
  );
}

export default Home;
