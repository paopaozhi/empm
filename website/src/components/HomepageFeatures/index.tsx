import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: '依赖管理',
    Svg: require('@site/static/img/团队构建应用程序.svg').default,
    description: (
      <>
        通过 <code>empm.toml</code> 文件管理项目中依赖，这个文件中列出来所需要的依赖包以及他们的版本。
      </>
    ),
  },
  {
    title: '构建依赖包',
    Svg: require('@site/static/img/小日常.svg').default,
    description: (
      <>
        通过 <code>empm build</code> 命令构建依赖包，构建后的依赖包会被放在 <code>empm_modules</code> 目录下。
      </>
    ),
  },
  {
    title: '项目模板',
    Svg: require('@site/static/img/建筑工单.svg').default,
    description: (
      <>
        通过 <code>empm init</code> 命令初始化项目模板，项目模板中包含了 <code>empm.toml</code> 文件。
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
