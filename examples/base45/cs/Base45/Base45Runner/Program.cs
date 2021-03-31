// Copyright 2021 De Staat der Nederlanden, Ministerie van Volksgezondheid, Welzijn en Sport.
// Licensed under the EUROPEAN UNION PUBLIC LICENCE v. 1.2
// SPDX-License-Identifier: EUPL-1.2

using System;

namespace NL.MinVWS.Encoding.Base45.Runner
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            var buffer = new byte[Convert.ToInt64(args[0])];
            new Random().NextBytes(buffer);
            Console.WriteLine(BitConverter.ToString(buffer));
            Console.WriteLine(new Base45Encoding().Encode(buffer));
        }
    }
}
