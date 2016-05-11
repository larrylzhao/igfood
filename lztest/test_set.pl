use strict;

open IN, "test_set.json";
my @fArr = <IN>;
close IN;

open OUT, ">test_set.out";
foreach my $line (@fArr) {
	my ($likes, $link, $lowres);
	if ($line =~ m/likes":"(\d+)/) {
		$likes = $1;
	}
	if ($line =~ m/lowres":"(.+)"/) {
		$lowres = $1;
	}
	if ($line =~ m/link":"(\d+)/) {
		$link = $1;
	}
	print OUT "$likes\t$lowres\t$link\n";
}