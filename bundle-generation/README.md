# Bundle Generation Scripts

These scripts are used to generate the template charts for the MultiClusterHub and MultiClusterEngine operator. When the team
onboards a new component into ACM or MCE, these are the scripts that are executed to generate a transformed chart for the
operators to render data for during runtime. These scripts are executed throughout the week as a github action in the
[multiclusterhub-operator](https://github.com/stolostron/multiclusterhub-operator.git) and [backplane-operator](https://github.com/stolostron/backplane-operator)

## Contributing

To update the scripts please ensure that you create a pull request and request for a review from one of the owners of the team.
These scripts are maintained by the ACM Hub Installer team; therefore, any unauthorized pull request will be rejected since it
could interfere with the automation that is responsible for building the charts for the different sub operators in ACM or MCE.

## Bundles to Charts

```bash
make regenerate-charts-from-bundles
```

## Generate Charts

```bash
make regenerate-charts
```

## Generate Sha Commits

```bash
make regenerate-operator-sha-commits
```

## Move Charts

```bash
make copy-charts
```
