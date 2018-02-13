#!/usr/bin/perl
use warnings; #sed replacement for -w perl parameter
# Copyright 2017   David Snyder
# Apache 2.0
#

if (@ARGV != 2) {
  print STDERR "Usage: $0 <path-to-yiwei> <path-to-output>\n";
  print STDERR "e.g. $0 export/ data/\n";
  exit(1);
}

($db_base, $out_dir) = @ARGV;

# Handle enroll, actually labeled data 
$out_dir_enroll = "$out_dir/yiwei_labeled";
if (system("mkdir -p $out_dir_enroll")) {
  die "Error making directory $out_dir_enroll";
}

$tmp_dir_enroll = "$out_dir_enroll/tmp";
if (system("mkdir -p $tmp_dir_enroll") != 0) {
  die "Error making directory $tmp_dir_enroll";
}

open(SPKR, ">$out_dir_enroll/utt2spk") || die "Could not open the output file $out_dir_enroll/utt2spk";
open(WAV, ">$out_dir_enroll/wav.scp") || die "Could not open the output file $out_dir_enroll/wav.scp";
# open(META, "<$db_base/docs/sre16_eval_enrollment.tsv") or die "cannot open wav list";
open(META, "<$db_base/docs/split_pcm_ndx") or die "cannot open wav list";
%utt2fixedutt = ();
while (<META>) {
  $line = $_;
  @toks = split(" ", $line);
  $spk = $toks[0];
  $utt = $toks[1];
  if ($utt ne "segment") {
    print SPKR "${spk}-${utt} $spk\n";
    $utt2fixedutt{$utt} = "${spk}-${utt}";
  }
}

if (system("find $db_base/data/labeled/ -name '*.wav' > $tmp_dir_enroll/sph.list") != 0) {
  die "Error getting list of sph files";
}

open(WAVLIST, "<$tmp_dir_enroll/sph.list") or die "cannot open wav list";

while(<WAVLIST>) {
  chomp;
  $sph = $_;
  @t = split("/",$sph);
  @t1 = split("[/]",$t[$#t]);
  $utt=$utt2fixedutt{$t1[0]};
  print WAV "$utt"," sox -t wav $sph -t wav  - |\n";
  #print WAV "$utt"," sph2pipe -f wav -p -c 1 $sph |\n";
}
close(WAV) || die;
close(SPKR) || die;

if (system("utils/utt2spk_to_spk2utt.pl $out_dir_enroll/utt2spk >$out_dir_enroll/spk2utt") != 0) {
  die "Error creating spk2utt file in directory $out_dir_enroll";
}
if (system("utils/fix_data_dir.sh $out_dir_enroll") != 0) {
  die "Error fixing data dir $out_dir_enroll";
}
